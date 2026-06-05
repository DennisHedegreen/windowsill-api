import asyncio
import json
import math
import os
import time
import hashlib
import sqlite3
import httpx
from collections import defaultdict
from contextlib import contextmanager
from pathlib import Path
from datetime import datetime
from fastapi import FastAPI, Query, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

DATABASE_URL = os.getenv("DATABASE_URL")  # set on Railway; absent → SQLite locally
_USE_PG = bool(DATABASE_URL)

if _USE_PG:
    import psycopg2
    import psycopg2.extras

# ── Version ────────────────────────────────────────────────────────────────────

API_VERSION = "0.2.0"
LIBRARY_VERSION = "2026-06-05"
SCORING_VERSION = "0.5.0"

# ── Config ─────────────────────────────────────────────────────────────────────

PLANTS_DIR = Path(os.getenv("PLANTS_DIR", str(Path(__file__).parent / "plants")))
DB_PATH = Path(__file__).parent / "keys.db"

MONTH_NAMES = ["", "January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]

RELIABLE_THRESHOLD = 0.55
OPTIMISTIC_RANGE = (0.35, 0.68)
RATE_LIMIT_NO_KEY = int(os.getenv("RATE_LIMIT_NO_KEY", "60"))  # per hour
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

PLAN_LIMITS = {
    "free": 1_000,
    "builder": 10_000,
    "pro": 100_000,
    "internal": None,
    "sponsored": None,
}

TYPE_LABELS = {"op": "open-pollinated", "heirloom": "heirloom", "hybrid": "hybrid"}
ORIENTATION_QUALITY = {"S": 1.0, "E": 0.75, "W": 0.75, "N": 0.35}

SAFETY_FLAGS: dict[str, dict] = {
    # Pennyroyal — toxic in high doses
    "WSL-0013": {
        "culinary_use": "caution",
        "warning": "Toxic in high doses. Not recommended as a primary culinary herb.",
        "score_penalty": 0.35,
    },
    # Comfrey — pyrrolizidine alkaloids, restricted internal use
    "WSL-0044": {
        "culinary_use": "restricted",
        "warning": "Internal use restricted in many countries due to pyrrolizidine alkaloids.",
        "score_penalty": 0.5,
    },
    # Russian Tarragon — culinarily inferior
    "WSL-0041": {
        "culinary_use": "inferior",
        "warning": "Considered culinarily inferior to French tarragon.",
        "score_penalty": 0.15,
    },
    # Tansy — toxic (thujone), not for culinary use
    "WSL-0130": {
        "culinary_use": "toxic",
        "warning": "Toxic — contains thujone. Not for culinary use.",
        "score_penalty": 0.6,
    },
    # Wormwood — toxic (thujone/absinthin), restricted culinary use
    "WSL-0129": {
        "culinary_use": "restricted",
        "warning": "Contains thujone (absinthin). Restricted culinary use — only trace amounts safe.",
        "score_penalty": 0.45,
    },
    # Mugwort — contains thujone, avoid in pregnancy
    "WSL-0128": {
        "culinary_use": "caution",
        "warning": "Contains thujone. Avoid in pregnancy. Not for regular culinary use.",
        "score_penalty": 0.35,
    },
    # Rue — phototoxic sap, restricted culinary use
    "WSL-0121": {
        "culinary_use": "caution",
        "warning": "Phototoxic sap — handle with gloves. Use only in tiny amounts as flavouring.",
        "score_penalty": 0.35,
    },
    # Motherwort — avoid in pregnancy
    "WSL-0124": {
        "culinary_use": "caution",
        "warning": "Avoid in pregnancy. Medicinal herb — not a culinary herb.",
        "score_penalty": 0.25,
    },
    # Elder — raw berries mildly toxic
    "WSL-0123": {
        "culinary_use": "caution",
        "warning": "Raw berries mildly toxic — must be cooked. Flowers and cooked berries safe.",
        "score_penalty": 0.1,
    },
}

# ── App ────────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Windowsill API",
    version=API_VERSION,
    description="Geo-climate edible plant growing recommendation API.",
    docs_url="/docs",
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_methods=["GET"],
    allow_headers=["*"],
)


# ── Error handlers ─────────────────────────────────────────────────────────────

@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    errors = []
    for e in exc.errors():
        field = ".".join(str(x) for x in e["loc"] if x != "query")
        errors.append({"field": field, "error": e["msg"]})
    return JSONResponse(status_code=422, content={
        "error": "invalid_parameters",
        "message": "One or more query parameters are invalid.",
        "details": errors,
    })


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(status_code=404, content={
        "error": "not_found",
        "message": getattr(exc, "detail", "Resource not found."),
    })


@app.exception_handler(500)
async def server_error_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={
        "error": "server_error",
        "message": "An unexpected error occurred.",
    })


# ── API key database ───────────────────────────────────────────────────────────

@contextmanager
def _db():
    if _USE_PG:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=psycopg2.extras.RealDictCursor)
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    else:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()


def _exec(conn, sql: str, params: tuple = ()):
    """Execute SQL with cross-backend parameter placeholder normalisation."""
    if _USE_PG:
        sql = sql.replace("?", "%s")
    cur = conn.cursor()
    cur.execute(sql, params)
    return cur


def init_keys_db():
    with _db() as conn:
        _exec(conn, """
            CREATE TABLE IF NOT EXISTS api_keys (
                key_hash      TEXT PRIMARY KEY,
                owner         TEXT NOT NULL,
                project       TEXT,
                plan          TEXT NOT NULL DEFAULT 'free',
                monthly_limit INTEGER,
                usage_month   TEXT,
                usage_count   INTEGER NOT NULL DEFAULT 0,
                active        INTEGER NOT NULL DEFAULT 1,
                expires_at    INTEGER,
                note          TEXT,
                created_at    INTEGER NOT NULL
            )
        """)


def _hash_key(key: str) -> str:
    return hashlib.sha256(key.encode()).hexdigest()


def _current_month() -> str:
    return time.strftime("%Y-%m")


def check_api_key(raw_key: str) -> tuple[bool, str]:
    h = _hash_key(raw_key)
    with _db() as conn:
        row = _exec(conn, "SELECT * FROM api_keys WHERE key_hash=?", (h,)).fetchone()
    if not row:
        return False, "invalid_key"
    row = dict(row)
    if not row["active"]:
        return False, "key_inactive"
    if row["expires_at"] and time.time() > row["expires_at"]:
        return False, "key_expired"
    month = _current_month()
    limit = row["monthly_limit"] if row["monthly_limit"] is not None else PLAN_LIMITS.get(row["plan"])
    with _db() as conn:
        if row["usage_month"] != month:
            _exec(conn, "UPDATE api_keys SET usage_month=?, usage_count=1 WHERE key_hash=?", (month, h))
        else:
            if limit is not None and row["usage_count"] >= limit:
                return False, "monthly_limit_reached"
            _exec(conn, "UPDATE api_keys SET usage_count=usage_count+1 WHERE key_hash=?", (h,))
    return True, "ok"


# ── Rate limiting (IP, no key) ─────────────────────────────────────────────────

_ip_buckets: dict[str, list[float]] = defaultdict(list)


def check_ip_rate(ip: str) -> tuple[bool, int]:
    now = time.time()
    cutoff = now - 3600
    bucket = [t for t in _ip_buckets[ip] if t > cutoff]
    _ip_buckets[ip] = bucket
    if len(bucket) >= RATE_LIMIT_NO_KEY:
        return False, 0
    _ip_buckets[ip].append(now)
    return True, RATE_LIMIT_NO_KEY - len(_ip_buckets[ip])


# ── Auth dependency ────────────────────────────────────────────────────────────

async def require_access(request: Request) -> dict:
    raw_key = request.headers.get("X-API-Key") or request.query_params.get("api_key")
    if raw_key:
        allowed, reason = check_api_key(raw_key)
        if not allowed:
            messages = {
                "invalid_key": "Invalid API key.",
                "key_inactive": "This API key has been deactivated.",
                "key_expired": "This API key has expired.",
                "monthly_limit_reached": (
                    "Monthly request limit reached. "
                    "Send an email to windowsill@hedegreenresearch.com for sponsored access."
                ),
            }
            status = 429 if "limit" in reason else 401
            raise HTTPException(status_code=status, detail=messages.get(reason, reason))
        return {"auth": "key"}

    # IP rate limiting is in-memory — resets on server restart. Acceptable for MVP.
    ip = request.client.host if request.client else "unknown"
    allowed, remaining = check_ip_rate(ip)
    if not allowed:
        raise HTTPException(
            status_code=429,
            detail=(
                "Rate limit reached (60 req/hour without key). "
                "Free API keys available — or email for sponsored access."
            ),
            headers={"Retry-After": "3600"},
        )
    return {"auth": "ip", "remaining": remaining}


# ── Plant library ──────────────────────────────────────────────────────────────

_plant_cache: list[dict] | None = None


def load_plants() -> list[dict]:
    global _plant_cache
    if _plant_cache is not None:
        return _plant_cache
    index = json.loads((PLANTS_DIR / "index.json").read_text())
    plants = []
    for filename in index["plants"]:
        path = PLANTS_DIR / filename
        if path.exists():
            plants.append(json.loads(path.read_text()))
    _plant_cache = plants
    return plants


# ── Climate ────────────────────────────────────────────────────────────────────

_climate_cache: dict[tuple, dict[int, float]] = {}


async def fetch_all_monthly_temps(lat: float, lng: float) -> dict[int, float] | None:
    key = (round(lat, 2), round(lng, 2))
    if key in _climate_cache:
        return _climate_cache[key]
    url = (
        "https://archive-api.open-meteo.com/v1/archive"
        f"?latitude={lat}&longitude={lng}"
        "&start_date=2003-01-01&end_date=2022-12-31"
        "&daily=temperature_2m_mean&timezone=UTC"
    )
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.get(url)
            r.raise_for_status()
            data = r.json()
        times = data["daily"]["time"]
        temps = data["daily"]["temperature_2m_mean"]
        buckets: dict[int, list[float]] = {m: [] for m in range(1, 13)}
        for d, t in zip(times, temps):
            if t is not None:
                buckets[int(d[5:7])].append(t)
        result = {m: round(sum(v) / len(v), 1) for m, v in buckets.items() if v}
        if result:
            _climate_cache[key] = result
        return result or None
    except Exception:
        return None


async def fetch_monthly_temp(lat: float, lng: float, month: int) -> float | None:
    all_months = await fetch_all_monthly_temps(lat, lng)
    return all_months.get(month) if all_months else None


def estimate_temp(lat: float, month: int) -> float:
    abs_lat = abs(lat)
    m = ((month - 1 + 6) % 12) + 1 if lat < 0 else month
    seasonal_amplitude = min(abs_lat * 0.4, 16)
    seasonal = math.cos(((m - 7) / 12) * 2 * math.pi) * seasonal_amplitude
    return round(27 - abs_lat * 0.55 + seasonal, 1)


def calc_sun_hours(lat: float, orientation: str, month: int) -> float:
    abs_lat = abs(lat)
    m = ((month - 1 + 6) % 12) + 1 if lat < 0 else month
    daylight = 12 + math.sin(((m - 3) / 12) * 2 * math.pi) * (abs_lat / 90 * 8)
    factors = ({"S": 0.1, "N": 0.7, "E": 0.4, "W": 0.4} if lat < 0
               else {"S": 0.7, "N": 0.1, "E": 0.4, "W": 0.4})
    return round(daylight * factors[orientation], 1)


def build_warnings(lat: float, data_confidence: str) -> list[str]:
    warnings = []
    abs_lat = abs(lat)
    if data_confidence != "high":
        warnings.append("Climate data estimated from latitude only. Results are approximate.")
    if abs_lat > 60:
        warnings.append("Extreme latitude: indoor growing conditions may differ strongly from outdoor baseline.")
        warnings.append("Recommendation should be treated as experimental.")
    elif abs_lat > 50:
        warnings.append("High latitude: seasonal variation is significant. Check month carefully.")
    return warnings


async def get_conditions(lat: float, lng: float, orientation: str, month: int) -> dict:
    temp = await fetch_monthly_temp(lat, lng, month)
    data_source = "Open-Meteo archive 2003–2022"
    data_confidence = "high"
    if temp is None:
        temp = estimate_temp(lat, month)
        data_source = "latitude estimate"
        data_confidence = "low"
    abs_lat = abs(lat)
    m_adj = ((month - 1 + 6) % 12) + 1 if lat < 0 else month
    daylight = round(12 + math.sin(((m_adj - 3) / 12) * 2 * math.pi) * (abs_lat / 90 * 8), 1)
    sun = calc_sun_hours(lat, orientation, month)
    return {
        "month": month,
        "month_name": MONTH_NAMES[month],
        "avg_temp": temp,
        "sun_hours_total": daylight,
        "sun_hours_direct": sun,
        "orientation": orientation,
        "data_source": data_source,
        "data_confidence": data_confidence,
        "warnings": build_warnings(lat, data_confidence),
        "indoor_note": "Outdoor climate normal used as baseline. Indoor windowsill temperature may differ.",
    }


# ── Scoring ────────────────────────────────────────────────────────────────────

def score_temp(temp: float, min_t: float, max_t: float, optimal: float) -> float:
    if temp < min_t or temp > max_t:
        return 0.0
    half_range = max((max_t - min_t) / 2, 1)
    # Quadratic penalty — small deviations score near 1.0, large deviations drop faster
    return max(0.0, 1 - (abs(temp - optimal) / half_range) ** 2)


def score_sun(sun: float, min_hours: float, optimistic: bool = False) -> float:
    threshold = min_hours * 0.7 if optimistic else min_hours * 0.5
    if sun < threshold:
        return 0.0
    return 1.0 if sun >= min_hours else sun / min_hours


def _label(v: float) -> str:
    if v >= 0.9: return "excellent"
    if v >= 0.72: return "good"
    if v >= 0.5: return "acceptable"
    if v > 0: return "weak"
    return "poor"


def score_plant(plant: dict, temp: float, sun: float, orientation: str,
                data_confidence: str, context: str = "windowsill",
                optimistic: bool = False, lat: float = 0.0,
                month: int = 6) -> dict:

    oq = ORIENTATION_QUALITY.get(orientation, 1.0)
    sun_req = plant.get("sun_direct", "full")
    sun_mod = 0.6 if (sun_req == "shade" and oq > 0.5) else (0.8 if (sun_req == "partial" and oq > 0.85) else 1.0)
    s_score = score_sun(sun, plant["sun_hours"], optimistic) * sun_mod

    habit = plant.get("habit", {})
    habit_val = habit.get(context, "good")
    habit_score = {"good": 1.0, "acceptable": 0.82, "risky": 0.55, "unsuitable": 0.0}.get(habit_val, 1.0)

    frost_note = None

    if context == "windowsill":
        # Indoors — outdoor temperature irrelevant. Score on sun + habit only.
        t_score = 1.0
        t_note = "indoor — outdoor temperature not used"
        plant_match = round(max(0.0, s_score * 0.6 + habit_score * 0.4), 2)
        confidence_factor = 1.0

    elif context == "balcony":
        # Outdoor container — temp matters but containers offer marginal protection.
        # Frost risk applies a penalty when frost is imminent (< 4 weeks).
        min_t = plant["min_temp"] - 3 if optimistic else plant["min_temp"]
        max_t = plant["max_temp"] + 3 if optimistic else plant["max_temp"]
        t_score = score_temp(temp, min_t, max_t, plant["optimal_temp"])
        t_note = None
        frost_weeks = weeks_until_frost(lat, month)
        if frost_weeks is not None and frost_weeks < 4:
            frost_penalty = max(0.0, (4 - frost_weeks) / 4) * 0.3
            t_score = max(0.0, t_score - frost_penalty)
            frost_note = f"Frost risk: ~{frost_weeks}w away — score reduced"
        # Balcony: temp 0.45 · sun 0.35 · habit 0.20
        plant_match = round(max(0.0, t_score * 0.45 + s_score * 0.35 + habit_score * 0.20), 2)
        confidence_factor = 1.0 if data_confidence == "high" else 0.75

    else:  # garden
        # Full outdoor exposure — no container buffer. Frost cutoff is stricter.
        # Plants rated unsuitable for garden context are already filtered by habit_score=0.
        min_t = plant["min_temp"] - 2 if optimistic else plant["min_temp"]
        max_t = plant["max_temp"] + 2 if optimistic else plant["max_temp"]
        t_score = score_temp(temp, min_t, max_t, plant["optimal_temp"])
        t_note = None
        frost_weeks = weeks_until_frost(lat, month)
        if frost_weeks is not None and frost_weeks < 6:
            frost_penalty = max(0.0, (6 - frost_weeks) / 6) * 0.4
            t_score = max(0.0, t_score - frost_penalty)
            frost_note = f"Frost risk: ~{frost_weeks}w away — score reduced"
        # Garden: temp 0.50 · sun 0.30 · habit 0.20
        plant_match = round(max(0.0, t_score * 0.50 + s_score * 0.30 + habit_score * 0.20), 2)
        confidence_factor = 1.0 if data_confidence == "high" else 0.75

    final = round(plant_match * confidence_factor, 2)

    safety = SAFETY_FLAGS.get(plant.get("id", ""))
    if not safety:
        # Auto-scan notes for safety signals not yet manually tagged
        notes_lower = (plant.get("notes", "") + " " + plant.get("contributor_note", "")).lower()
        if any(kw in notes_lower for kw in ("not for culinary use", "toxic in large", "phototoxic")):
            safety = {
                "culinary_use": "caution",
                "warning": "Note: this plant may not be safe for culinary use — check before consuming.",
                "score_penalty": 0.3,
            }
    if safety:
        final = round(max(0.0, final - safety["score_penalty"]), 2)

    temp_breakdown = {"label": _label(t_score), "score": round(t_score, 2),
                      "actual_c": temp, "optimal_c": plant["optimal_temp"]}
    if context == "windowsill":
        temp_breakdown["note"] = "indoor — outdoor temperature not used"
    if frost_note:
        temp_breakdown["frost_note"] = frost_note

    return {
        "match_score": final,
        "scores": {
            "plant_match": plant_match,
            "data_confidence": confidence_factor,
            "final_confidence": final,
        },
        "score_breakdown": {
            "temperature": temp_breakdown,
            "sun": {"label": _label(s_score), "score": round(s_score, 2),
                    "actual_hours": sun, "required_hours": plant["sun_hours"],
                    "sun_direct_req": sun_req, "orientation_quality": oq},
            "context": {"label": "good", "score": 1.0},
            "habit": {"label": habit_val, "score": habit_score, "note": habit.get("note", "")},
        },
        "safety": {"culinary_use": safety["culinary_use"], "warning": safety["warning"]} if safety else None,
        "data_warning": "Plant data is seeded and needs source verification." if "Needs primary source" in plant.get("contributor_note", "") else None,
    }


def _enrich(plant: dict, score_result: dict) -> dict:
    return {
        **plant,
        "common_group": plant.get("species"),
        "type_label": TYPE_LABELS.get(plant.get("type", ""), plant.get("type", "")),
        **score_result,
    }


def weeks_until_frost(lat: float, month: int) -> int | None:
    """Rough estimate of weeks until first frost based on latitude and current month.
    Returns None if frost is not expected (tropical/subtropical climates)."""
    abs_lat = abs(lat)
    if abs_lat < 25:
        return None  # frost unlikely
    # Approximate first frost month based on latitude
    if abs_lat >= 60:
        first_frost_month = 9   # September
    elif abs_lat >= 50:
        first_frost_month = 10  # October
    elif abs_lat >= 40:
        first_frost_month = 11  # November
    else:
        first_frost_month = 12  # December

    # Southern hemisphere: flip
    if lat < 0:
        first_frost_month = ((first_frost_month + 5) % 12) + 1

    if month <= first_frost_month:
        return (first_frost_month - month) * 4
    return None  # past frost already — next year


def coldest_month_temp(lat: float) -> float:
    """Estimate of the average coldest month minimum temperature from latitude.
    Calibrated to USDA zone boundaries — used when Open-Meteo data is unavailable."""
    abs_lat = abs(lat)
    if abs_lat >= 70: return -30.0  # zone 4/5 — Arctic/subarctic
    if abs_lat >= 60: return -18.0  # zone 7   — N. Scandinavia, S. Alaska
    if abs_lat >= 55: return -12.0  # zone 8   — Denmark, Scotland, S. Scandinavia
    if abs_lat >= 50: return  -7.0  # zone 9   — N. Germany, S. England, Benelux
    if abs_lat >= 45: return  -1.0  # zone 10  — N. France, N. Italy, Vancouver
    if abs_lat >= 40: return   5.0  # zone 11  — Madrid, Istanbul, N. California
    if abs_lat >= 30: return  12.0  # zone 12  — N. Africa, S. Japan, S. Texas
    if abs_lat >= 20: return  18.0  # zone 12/13
    return 22.0                      # zone 13  — Tropical


def usda_zone_from_temp(min_winter_temp: float) -> int:
    if min_winter_temp <= -34: return 4
    if min_winter_temp <= -29: return 5
    if min_winter_temp <= -23: return 6
    if min_winter_temp <= -18: return 7
    if min_winter_temp <= -12: return 8
    if min_winter_temp <= -7:  return 9
    if min_winter_temp <= -1:  return 10
    if min_winter_temp <= 4:   return 11
    if min_winter_temp <= 10:  return 12
    return 13


def overwinter_assessment(plant: dict, location_zone: int) -> dict:
    """Assess whether the plant can overwinter at this location's USDA zone."""
    plant_zone = plant.get("hardiness_zone_min", 10)  # now derived from hardiness_temp, not min_temp
    if plant_zone <= location_zone:
        return {"status": "yes", "plant_zone": plant_zone, "location_zone": location_zone}
    elif plant_zone == location_zone + 1:
        return {"status": "marginal", "plant_zone": plant_zone, "location_zone": location_zone,
                "note": f"Zone {plant_zone} plant at zone {location_zone} location — may survive mild winters with protection."}
    else:
        return {"status": "no", "plant_zone": plant_zone, "location_zone": location_zone,
                "note": f"Annual only at this location — cannot overwinter outdoors (zone {plant_zone} plant, zone {location_zone} here)."}


def timing_assessment(plant: dict, start_type: str, month: int, lat: float) -> dict:
    """Assess whether there is enough time to harvest before frost/winter."""
    weeks_needed = (plant.get("weeks_from_transplant") or plant.get("grow_time_weeks", 8)
                    if start_type == "plant"
                    else plant.get("grow_time_weeks", 8))

    frost_weeks = weeks_until_frost(lat, month)

    if frost_weeks is None:
        return {"status": "ok", "note": "No frost expected — year-round growing possible."}

    # Frost-hardy plants are not blocked by frost — they grow through it.
    # hardiness_temp <= -2°C means the plant survives freezing temperatures.
    frost_hardy = plant.get("hardiness_temp", 0) <= -2

    if frost_hardy and frost_weeks is not None and frost_weeks < weeks_needed:
        # Enough time to establish before frost, and plant survives winter
        if frost_weeks >= max(2, weeks_needed // 3):
            return {"status": "ok", "note": f"Frost-hardy — grows through winter. Get established before frost (~{frost_weeks}w away)."}
        else:
            return {"status": "tight", "note": f"Frost-hardy but little time to establish — only ~{frost_weeks}w before frost. Start promptly."}

    if frost_weeks >= weeks_needed + 2:
        return {"status": "ok", "note": f"Enough time — harvest expected ~{weeks_needed}w, frost ~{frost_weeks}w away."}
    elif frost_weeks >= weeks_needed:
        return {"status": "tight", "note": f"Tight timing — harvest ~{weeks_needed}w, frost ~{frost_weeks}w away. Start promptly."}
    else:
        return {"status": "too_late", "note": f"Too late to start from {'transplant' if start_type == 'plant' else 'seed'} — needs {weeks_needed}w but only ~{frost_weeks}w before frost."}


def filter_and_score(plants: list[dict], context: str, temp: float, sun: float,
                     orientation: str, data_confidence: str, mode: str,
                     species: str | None, variety_type: str | None,
                     start_type: str = "seed", lat: float = 0.0,
                     month: int = 6) -> dict:
    candidates = [p for p in plants if context in p.get("context", [])]
    if species:
        candidates = [p for p in candidates if p.get("species") == species]
    if variety_type:
        candidates = [p for p in candidates if p.get("type") == variety_type]

    winter_temp = coldest_month_temp(lat)
    location_zone = usda_zone_from_temp(winter_temp)

    def _score_and_enrich(p, optimistic=False):
        result = score_plant(p, temp, sun, orientation, data_confidence, context, optimistic, lat, month)
        enriched = _enrich(p, result)
        enriched["timing"] = timing_assessment(p, start_type, month, lat)
        enriched["start_type"] = start_type
        enriched["weeks_to_harvest"] = (
            p.get("weeks_from_transplant") or p.get("grow_time_weeks", 8)
            if start_type == "plant"
            else p.get("grow_time_weeks", 8)
        )
        if context in ("balcony", "garden"):
            enriched["overwinter"] = overwinter_assessment(p, location_zone)
        return enriched

    TIMING_RANK = {"ok": 0, "tight": 1, "year_round": 0, "too_late": 2}

    def _sort_key(p):
        timing_rank = TIMING_RANK.get(p.get("timing", {}).get("status", "ok"), 2)
        weeks = p.get("weeks_to_harvest") or p.get("grow_time_weeks", 99)
        return (-p["match_score"], timing_rank, weeks)

    all_scored = sorted(
        [_score_and_enrich(p) for p in candidates],
        key=_sort_key
    )
    reliable = [p for p in all_scored if p["match_score"] >= RELIABLE_THRESHOLD]
    weak = [p for p in all_scored if p["match_score"] < RELIABLE_THRESHOLD]

    if mode == "top10":
        return {
            "results": reliable[:10],
            "hidden_weak": len(weak),
            "mode_note": f"Up to 10 reliable recommendations (final_confidence ≥ {RELIABLE_THRESHOLD}). {len(weak)} weak match{'es' if len(weak) != 1 else ''} hidden.",
            "empty_state": None if reliable else {
                "title": "No reliable recommendations",
                "message": "No herbs passed the reliability threshold for this location, orientation and month.",
                "suggestions": ["Try a south-facing window", "Try a warmer month",
                                "Use optimistic mode for stretch options", "Use all mode to inspect weak matches"],
            },
        }

    if mode == "optimal":
        return {
            "results": reliable[:1],
            "hidden_weak": len(all_scored) - (1 if reliable else 0),
            "mode_note": "Single best reliable recommendation." if reliable else "No reliable optimal recommendation for these conditions.",
            "empty_state": None if reliable else {
                "title": "No reliable optimal pick",
                "message": "The best available match did not pass the confidence threshold.",
                "suggestions": ["Use optimistic mode for a stretch suggestion", "Try a different orientation or month"],
            },
        }

    if mode == "optimistic":
        opt_scored = sorted(
            [_score_and_enrich(p, optimistic=True) for p in candidates],
            key=lambda x: x["match_score"], reverse=True
        )
        stretch = [p for p in opt_scored if OPTIMISTIC_RANGE[0] <= p["match_score"] <= OPTIMISTIC_RANGE[1]]
        pick = (stretch or opt_scored or [None])[0]
        if pick:
            bd = pick.get("score_breakdown", {})
            needs = []
            t = bd.get("temperature", {})
            s = bd.get("sun", {})
            h = bd.get("habit", {})
            if t.get("label") in ("weak", "acceptable"):
                needs.append("warmer indoor location" if t.get("actual_c", 0) < t.get("optimal_c", 20) else "cooler position away from direct heat")
            if s.get("label") in ("weak", "acceptable"):
                needs.append("grow light or brighter window")
            if h.get("label") in ("acceptable", "risky"):
                needs.append("good drainage and appropriate pot size")
            pick = {**pick, "could_work_if": needs or ["conditions are close — try it"]}
        return {
            "results": [pick] if pick else [],
            "hidden_weak": 0,
            "mode_note": "Stretch recommendation — may work with some adjustment.",
            "empty_state": None,
        }

    # all
    return {
        "results": all_scored,
        "hidden_weak": 0,
        "mode_note": "All ranked matches including weak and unsuitable. Research/debug mode.",
        "empty_state": None,
    }


# ── Version helper ─────────────────────────────────────────────────────────────

def version_block() -> dict:
    return {
        "api_version": API_VERSION,
        "library_version": LIBRARY_VERSION,
        "scoring_version": SCORING_VERSION,
    }


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.get("/v1/health")
async def health():
    return {
        **version_block(),
        "status": "ok",
        "plant_count": len(load_plants()),
        "climate_cache_size": len(_climate_cache),
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


@app.get("/v1/recommend")
async def recommend(
    lat: float = Query(..., ge=-90, le=90),
    lng: float = Query(..., ge=-180, le=180),
    orientation: str = Query(..., pattern="^[NSEW]$"),
    context: str = Query(..., pattern="^(windowsill|balcony|garden)$"),
    month: int = Query(default=0, ge=0, le=12),
    mode: str = Query(default="top10", pattern="^(all|top10|optimal|optimistic)$"),
    species: str | None = Query(default=None),
    type: str | None = Query(default=None),
    start_type: str = Query(default="seed", pattern="^(seed|plant)$"),
    _access: dict = Depends(require_access),
):
    m = month if month > 0 else datetime.now().month
    cond = await get_conditions(lat, lng, orientation, m)
    plants = load_plants()
    scored = filter_and_score(plants, context, cond["avg_temp"], cond["sun_hours_direct"],
                              orientation, cond["data_confidence"], mode, species, type,
                              start_type=start_type, lat=lat, month=m)
    location_zone = usda_zone_from_temp(coldest_month_temp(lat))
    return {
        **version_block(),
        "location": {"lat": lat, "lng": lng},
        "conditions": {**cond, "context": context},
        "location_zone": {"usda": location_zone, "basis": "latitude estimate"},
        "mode": mode,
        "start_type": start_type,
        "mode_note": scored["mode_note"],
        "result_type": "estimated" if cond["data_confidence"] != "high" else "standard",
        "count": len(scored["results"]),
        "hidden_weak": scored["hidden_weak"],
        "empty_state": scored["empty_state"],
        "recommendations": scored["results"],
    }


@app.get("/v1/calendar")
async def calendar(
    lat: float = Query(..., ge=-90, le=90),
    lng: float = Query(..., ge=-180, le=180),
    orientation: str = Query(..., pattern="^[NSEW]$"),
    context: str = Query(..., pattern="^(windowsill|balcony|garden)$"),
    mode: str = Query(default="optimal", pattern="^(all|top10|optimal|optimistic)$"),
    species: str | None = Query(default=None),
    type: str | None = Query(default=None),
    start_type: str = Query(default="seed", pattern="^(seed|plant)$"),
    _access: dict = Depends(require_access),
):
    plants = load_plants()
    all_temps = await fetch_all_monthly_temps(lat, lng)
    abs_lat = abs(lat)

    months = []
    for m in range(1, 13):
        temp = all_temps.get(m) if all_temps else None
        confidence = "high" if temp is not None else "low"
        if temp is None:
            temp = estimate_temp(lat, m)
        m_adj = ((m - 1 + 6) % 12) + 1 if lat < 0 else m
        daylight = round(12 + math.sin(((m_adj - 3) / 12) * 2 * math.pi) * (abs_lat / 90 * 8), 1)
        sun = calc_sun_hours(lat, orientation, m)
        scored = filter_and_score(plants, context, temp, sun, orientation, confidence, mode, species, type,
                                  start_type=start_type, lat=lat, month=m)
        best = scored["results"][0] if scored["results"] else None
        months.append({
            "month": m,
            "month_name": MONTH_NAMES[m],
            "avg_temp": temp,
            "sun_hours_direct": sun,
            "data_confidence": confidence,
            "recommendation": best,
        })

    overall = "high" if all(m["data_confidence"] == "high" for m in months) else "mixed"
    return {
        **version_block(),
        "location": {"lat": lat, "lng": lng},
        "orientation": orientation,
        "context": context,
        "mode": mode,
        "data_confidence": overall,
        "calendar": months,
    }


@app.get("/v1/conditions")
async def conditions(
    lat: float = Query(..., ge=-90, le=90),
    lng: float = Query(..., ge=-180, le=180),
    orientation: str = Query(..., pattern="^[NSEW]$"),
    month: int = Query(default=0, ge=0, le=12),
    _access: dict = Depends(require_access),
):
    m = month if month > 0 else datetime.now().month
    cond = await get_conditions(lat, lng, orientation, m)
    return {**version_block(), "location": {"lat": lat, "lng": lng}, **cond}


@app.get("/v1/varieties")
async def varieties(
    species: str | None = Query(default=None),
    type: str | None = Query(default=None),
    context: str | None = Query(default=None),
    _access: dict = Depends(require_access),
):
    plants = load_plants()
    if species:
        plants = [p for p in plants if p.get("species") == species]
    if type:
        plants = [p for p in plants if p.get("type") == type]
    if context:
        plants = [p for p in plants if context in p.get("context", [])]
    return {**version_block(), "count": len(plants), "varieties": plants}


@app.get("/v1/varieties/{plant_id}")
async def variety(plant_id: str, _access: dict = Depends(require_access)):
    plants = load_plants()
    match = next((p for p in plants if p.get("id") == plant_id), None)
    if not match:
        raise HTTPException(status_code=404, detail=f"Variety {plant_id} not found.")
    return {**version_block(), **match}


@app.get("/v1/status")
async def status():
    plants = load_plants()
    return {
        **version_block(),
        "status": "ok",
        "plant_count": len(plants),
        "climate_cache_size": len(_climate_cache),
    }


@app.get("/v1/library")
async def library(
    context: str | None = Query(default=None, pattern="^(windowsill|balcony|garden)$"),
    _access: dict = Depends(require_access),
):
    plants = load_plants()
    if context:
        plants = [p for p in plants if context in p.get("context", [])]
    species = sorted({p.get("species") for p in plants if p.get("species")})
    return {
        **version_block(),
        "count": len(plants),
        "species_count": len(species),
        "species": species,
        "plants": plants,
    }


@app.get("/")
async def root():
    return {
        **version_block(),
        "name": "Windowsill API",
        "status": "ok",
        "docs": "/docs",
        "health": "/v1/health",
        "endpoints": [
            "GET /v1/health",
            "GET /v1/status",
            "GET /v1/recommend",
            "GET /v1/calendar",
            "GET /v1/conditions",
            "GET /v1/library",
            "GET /v1/varieties",
            "GET /v1/varieties/{id}",
        ],
        "access": {
            "no_key": f"{RATE_LIMIT_NO_KEY} requests/hour per IP",
            "free_key": "1,000 requests/month",
            "builder_key": "10,000 requests/month",
            "sponsored": "Email windowsill@hedegreenresearch.com",
        },
    }


# ── Startup ────────────────────────────────────────────────────────────────────

@app.on_event("startup")
async def startup():
    init_keys_db()
    load_plants()  # warm cache on startup
