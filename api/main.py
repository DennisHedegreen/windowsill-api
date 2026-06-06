import asyncio
import json
import math
import os
import re
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

API_VERSION = "0.6.0"
LIBRARY_VERSION = "2026-06-05"
SCORING_VERSION = "0.8.0"

# ── Config ─────────────────────────────────────────────────────────────────────

_HERE = Path(__file__).parent
PLANTS_DIR = (_HERE.parent / "plants") if (_HERE.parent / "plants").exists() else (_HERE / "plants")
DB_PATH = Path(__file__).parent / "keys.db"

MONTH_NAMES = ["", "January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]

RELIABLE_THRESHOLD = 0.55
OPTIMISTIC_RANGE = (0.35, 0.68)
RATE_LIMIT_NO_KEY = int(os.getenv("RATE_LIMIT_NO_KEY", "60"))  # per hour
_cors_env = os.getenv("CORS_ORIGINS", "*")
CORS_ORIGINS = ["*"] if _cors_env.strip() == "*" else _cors_env.split(",")
DEFAULT_CORS_ORIGIN_REGEX = r"^https://(www\.)?hedegreenresearch\.com$|^http://(localhost|127\.0\.0\.1):\d+$"
CORS_ORIGIN_REGEX = os.getenv("CORS_ORIGIN_REGEX", DEFAULT_CORS_ORIGIN_REGEX).strip() or None
_CORS_ORIGIN_RE = re.compile(CORS_ORIGIN_REGEX) if CORS_ORIGIN_REGEX else None

PLAN_LIMITS = {
    "free": 1_000,
    "builder": 10_000,
    "pro": 100_000,
    "internal": None,
    "sponsored": None,
}

TYPE_LABELS = {"op": "open-pollinated", "heirloom": "heirloom", "hybrid": "hybrid"}
ORIENTATION_QUALITY = {
    "S": 1.0, "SE": 0.90, "SW": 0.90,
    "E": 0.75, "W": 0.75,
    "NE": 0.50, "NW": 0.50,
    "N": 0.35,
}

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
    allow_origin_regex=CORS_ORIGIN_REGEX,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
    allow_credentials=False,
)


# ── CORS preflight catch-all ───────────────────────────────────────────────────

def cors_origin_for_request(request: Request) -> str:
    origin = request.headers.get("origin")
    if not origin:
        return "*"
    if "*" in CORS_ORIGINS or origin in CORS_ORIGINS:
        return origin
    if _CORS_ORIGIN_RE and _CORS_ORIGIN_RE.match(origin):
        return origin
    return "null"


@app.options("/{rest_of_path:path}")
async def preflight(rest_of_path: str, request: Request):
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": cors_origin_for_request(request),
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Max-Age": "600",
        },
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

_climate_cache: dict[tuple, dict] = {}  # key → {"months": {1..12}, "weeks": {1..53}, "elevation": float|None}


def _iso_week(date_str: str) -> int:
    from datetime import date
    d = date(int(date_str[:4]), int(date_str[5:7]), int(date_str[8:10]))
    return d.isocalendar()[1]


async def fetch_all_monthly_temps(lat: float, lng: float) -> dict | None:
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
        month_buckets: dict[int, list[float]] = {m: [] for m in range(1, 13)}
        week_buckets: dict[int, list[float]] = {w: [] for w in range(1, 54)}
        for d, t in zip(times, temps):
            if t is not None:
                month_buckets[int(d[5:7])].append(t)
                week_buckets[_iso_week(d)].append(t)
        months = {m: round(sum(v) / len(v), 1) for m, v in month_buckets.items() if v}
        weeks = {w: round(sum(v) / len(v), 1) for w, v in week_buckets.items() if v}
        elevation = data.get("elevation")
        if elevation is not None:
            elevation = round(float(elevation), 1)
        if months:
            result = {"months": months, "weeks": weeks, "elevation": elevation}
            _climate_cache[key] = result
            return result
        return None
    except Exception:
        return None


async def fetch_monthly_temp(lat: float, lng: float, month: int) -> float | None:
    data = await fetch_all_monthly_temps(lat, lng)
    return data["months"].get(month) if data else None


async def fetch_elevation(lat: float, lng: float) -> float | None:
    data = await fetch_all_monthly_temps(lat, lng)
    return data["elevation"] if data else None


def iso_week_to_day_of_year(week: int) -> float:
    """Mid-point day of year for an ISO week (week 1 ≈ day 4, each week = 7 days)."""
    return (week - 1) * 7 + 4


def week_to_month(week: int) -> int:
    """Approximate month for a given ISO week number."""
    from datetime import date
    # Use a non-leap year; week 53 maps to January of next year → return 12
    try:
        d = date.fromisocalendar(2015, min(week, 52), 4)
        return d.month
    except Exception:
        return 12


def estimate_temp_by_doy(lat: float, doy: float) -> float:
    """Estimate temperature from day-of-year (1–365) instead of month mid-point."""
    abs_lat = abs(lat)
    # Southern hemisphere: shift by 182 days
    d = (doy + 182) % 365 if lat < 0 else doy
    seasonal_amplitude = min(abs_lat * 0.4, 16)
    seasonal = math.cos(((d - 196) / 365) * 2 * math.pi) * seasonal_amplitude
    return round(27 - abs_lat * 0.55 + seasonal, 1)


def estimate_temp(lat: float, month: int) -> float:
    doy = (month - 1) * 30.4 + 15
    return estimate_temp_by_doy(lat, doy)


_COMPASS_NEIGHBORS = {
    "N":  ("NW", "NE"), "NE": ("N",  "E"),  "E":  ("NE", "SE"),
    "SE": ("E",  "S"),  "S":  ("SE", "SW"), "SW": ("S",  "W"),
    "W":  ("SW", "NW"), "NW": ("W",  "N"),
}


def _orientation_factor(lat: float, orientation: str) -> dict:
    return (
        {"S": 0.10, "SE": 0.25, "SW": 0.25, "E": 0.40, "W": 0.40, "NE": 0.55, "NW": 0.55, "N": 0.70}
        if lat < 0 else
        {"S": 0.70, "SE": 0.55, "SW": 0.55, "E": 0.40, "W": 0.40, "NE": 0.25, "NW": 0.25, "N": 0.10}
    )


def calc_sun_hours_by_doy(lat: float, orientation: str, doy: float,
                          context: str = "windowsill") -> float:
    abs_lat = abs(lat)
    d = (doy + 182) % 365 if lat < 0 else doy
    daylight = 12 + math.sin(((d - 80) / 365) * 2 * math.pi) * (abs_lat / 90 * 8)
    factors = _orientation_factor(lat, orientation)

    if context == "garden":
        # Open sky — orientation irrelevant, ~85% of full daylight (terrain/tree margin)
        return round(daylight * 0.85, 1)

    if context == "balcony":
        # Primary face 60%, each neighbor side 20% — open on 3 sides
        n1, n2 = _COMPASS_NEIGHBORS[orientation]
        combined = factors[orientation] * 0.60 + factors[n1] * 0.20 + factors[n2] * 0.20
        return round(daylight * combined, 1)

    # windowsill — direct face only
    return round(daylight * factors[orientation], 1)


def calc_sun_hours(lat: float, orientation: str, month: int,
                   context: str = "windowsill") -> float:
    doy = (month - 1) * 30.4 + 15
    return calc_sun_hours_by_doy(lat, orientation, doy, context)


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


def week_label(week: int, month: int) -> str:
    week_in_month = ((week - 1) % 4) + 1
    labels = ["early", "mid", "late", "late"]
    return f"Week {week} ({labels[week_in_month - 1]} {MONTH_NAMES[month]})"


async def get_conditions(lat: float, lng: float, orientation: str,
                         month: int, week: int | None = None,
                         context: str = "windowsill") -> dict:
    climate_data = await fetch_all_monthly_temps(lat, lng)
    data_source = "Open-Meteo archive 2003–2022"
    data_confidence = "high"
    elevation = None

    if week is not None:
        doy = iso_week_to_day_of_year(week)
        if climate_data:
            temp = climate_data["weeks"].get(week)
            elevation = climate_data["elevation"]
        else:
            temp = None
        if temp is None:
            temp = estimate_temp_by_doy(lat, doy)
            data_source = "latitude estimate"
            data_confidence = "low"
        sun = calc_sun_hours_by_doy(lat, orientation, doy, context)
        abs_lat = abs(lat)
        d_adj = (doy + 182) % 365 if lat < 0 else doy
        daylight = round(12 + math.sin(((d_adj - 80) / 365) * 2 * math.pi) * (abs_lat / 90 * 8), 1)
    else:
        doy = None
        if climate_data:
            temp = climate_data["months"].get(month)
            elevation = climate_data["elevation"]
        else:
            temp = None
        if temp is None:
            temp = estimate_temp(lat, month)
            data_source = "latitude estimate"
            data_confidence = "low"
        sun = calc_sun_hours(lat, orientation, month, context)
        abs_lat = abs(lat)
        m_adj = ((month - 1 + 6) % 12) + 1 if lat < 0 else month
        daylight = round(12 + math.sin(((m_adj - 3) / 12) * 2 * math.pi) * (abs_lat / 90 * 8), 1)

    # Elevation lapse rate: −0.6°C per 100m
    if elevation and elevation > 0:
        temp = round(temp - (elevation / 100) * 0.6, 1)

    result = {
        "month": month,
        "month_name": MONTH_NAMES[month],
        "avg_temp": temp,
        "sun_hours_total": daylight,
        "sun_hours_direct": sun,
        "orientation": orientation,
        "elevation": elevation,
        "data_source": data_source,
        "data_confidence": data_confidence,
        "warnings": build_warnings(lat, data_confidence),
        "indoor_note": "Outdoor climate normal used as baseline. Indoor windowsill temperature may differ.",
    }
    if week is not None:
        result["week"] = week
        result["week_label"] = week_label(week, month)
    return result


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


def could_work_text(plant: dict, conditions: dict) -> str:
    timing = plant.get("timing", {})
    habit = plant.get("score_breakdown", {}).get("habit", {})
    parts = []
    sun_hours = conditions.get("sun_hours_direct")
    orientation = conditions.get("orientation")
    context = conditions.get("context")
    if sun_hours is not None and orientation and context:
        parts.append(f"{round(sun_hours, 1)}h direct {orientation}-facing light for a {context}.")
    if timing.get("status") in ("ok", "year_round") and timing.get("note"):
        parts.append(timing["note"])
    elif plant.get("weeks_to_harvest"):
        parts.append(f"Harvest expected in ~{plant['weeks_to_harvest']}w under suitable care.")
    if habit.get("label") == "good" and habit.get("note"):
        parts.append(habit["note"])
    return " ".join(parts) or "Conditions are within the current matching band."


def likely_failure_text(plant: dict) -> str:
    safety = plant.get("safety")
    if safety and safety.get("warning"):
        return safety["warning"]

    timing = plant.get("timing", {})
    if timing.get("status") in ("tight", "too_late") and timing.get("note"):
        return timing["note"]

    breakdown = plant.get("score_breakdown", {})
    temp = breakdown.get("temperature", {})
    sun = breakdown.get("sun", {})
    habit = breakdown.get("habit", {})
    if temp.get("label") in ("weak", "poor"):
        actual = temp.get("actual_c")
        optimal = temp.get("optimal_c")
        if actual is not None and optimal is not None:
            return f"Temperature is the weak point: {actual}°C baseline against ~{optimal}°C optimal."
        return "Temperature is the weak point."
    if sun.get("label") in ("weak", "poor"):
        actual = sun.get("actual_hours")
        required = sun.get("required_hours")
        if actual is not None and required is not None:
            return f"Light is the weak point: {actual}h direct sun against ~{required}h required."
        return "Light is the weak point."
    if habit.get("note"):
        return habit["note"]
    if plant.get("data_warning"):
        return plant["data_warning"]
    return "No single failure point is identified by the current prototype profile."


def rima_recommendation(plant: dict, conditions: dict) -> dict:
    return {
        "id": plant.get("id"),
        "name": plant.get("name_en") or plant.get("name_latin") or plant.get("id"),
        "local_name": plant.get("name_da") or plant.get("name_en") or plant.get("name_latin"),
        "latin": plant.get("name_latin"),
        "species": plant.get("species"),
        "type": plant.get("type"),
        "type_label": plant.get("type_label"),
        "could_work": could_work_text(plant, conditions),
        "likely_failure": likely_failure_text(plant),
        "grow_time_weeks": plant.get("weeks_to_harvest") or plant.get("grow_time_weeks"),
        "match_score": plant.get("match_score"),
        "timing": plant.get("timing"),
        "safety": plant.get("safety"),
        "data_warning": plant.get("data_warning"),
    }


def rima_response(payload: dict) -> dict:
    conditions = payload["conditions"]
    return {
        **version_block(),
        "format": "rima",
        "location": payload["location"],
        "conditions": {
            "week": conditions.get("week"),
            "week_label": conditions.get("week_label"),
            "month": conditions.get("month"),
            "month_name": conditions.get("month_name"),
            "avg_temp": conditions.get("avg_temp"),
            "sun_hours_direct": conditions.get("sun_hours_direct"),
            "orientation": conditions.get("orientation"),
            "context": conditions.get("context"),
            "data_source": conditions.get("data_source"),
            "data_confidence": conditions.get("data_confidence"),
            "warnings": conditions.get("warnings", []),
            "indoor_note": conditions.get("indoor_note"),
        },
        "location_zone": payload["location_zone"],
        "start_type": payload["start_type"],
        "result_type": payload["result_type"],
        "count": payload["count"],
        "total_qualified": payload["total_qualified"],
        "hidden_weak": payload["hidden_weak"],
        "empty_state": payload["empty_state"],
        "recommendations": [
            rima_recommendation(plant, conditions)
            for plant in payload["recommendations"]
        ],
    }


def first_frost_week(lat: float) -> int | None:
    """ISO week of typical first frost. Returns None for tropical climates."""
    abs_lat = abs(lat)
    if abs_lat < 25:
        return None
    if abs_lat >= 60:
        frost_week = 36   # ~early September
    elif abs_lat >= 50:
        frost_week = 42   # ~mid October
    elif abs_lat >= 40:
        frost_week = 46   # ~mid November
    else:
        frost_week = 50   # ~mid December
    # Southern hemisphere: shift by 26 weeks
    if lat < 0:
        frost_week = ((frost_week + 26 - 1) % 52) + 1
    return frost_week


def weeks_until_frost(lat: float, month: int, week: int | None = None) -> int | None:
    """Weeks until first frost. Uses ISO week when available for precision."""
    frost_week = first_frost_week(lat)
    if frost_week is None:
        return None
    if week is not None:
        if week <= frost_week:
            return frost_week - week
        return None  # past frost — next year
    # Month-based fallback
    current_week = (month - 1) * 4 + 2
    if current_week <= frost_week:
        return frost_week - current_week
    return None


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


def timing_assessment(plant: dict, start_type: str, month: int, lat: float,
                      week: int | None = None) -> dict:
    """Assess whether there is enough time to harvest before frost/winter."""
    weeks_needed = (plant.get("weeks_from_transplant") or plant.get("grow_time_weeks", 8)
                    if start_type == "plant"
                    else plant.get("grow_time_weeks", 8))

    frost_weeks = weeks_until_frost(lat, month, week)

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
                     orientation: str, data_confidence: str,
                     species: str | None, variety_type: str | None,
                     start_type: str = "seed", lat: float = 0.0,
                     month: int = 6, winter_min_temp: float | None = None,
                     week: int | None = None,
                     limit: int = 10, min_score: float = RELIABLE_THRESHOLD,
                     optimistic: bool = False, shuffle: bool = False,
                     pool: int = 30,
                     exclude: list[str] | None = None) -> dict:
    candidates = [p for p in plants if context in p.get("context", [])]
    if species:
        candidates = [p for p in candidates if p.get("species") == species]
    if variety_type:
        candidates = [p for p in candidates if p.get("type") == variety_type]
    if exclude:
        candidates = [p for p in candidates if p.get("id") not in exclude]

    winter_temp = winter_min_temp if winter_min_temp is not None else coldest_month_temp(lat)
    location_zone = usda_zone_from_temp(winter_temp)

    def _score_and_enrich(p):
        result = score_plant(p, temp, sun, orientation, data_confidence, context, optimistic, lat, month)
        enriched = _enrich(p, result)
        enriched["timing"] = timing_assessment(p, start_type, month, lat, week)
        enriched["start_type"] = start_type
        enriched["weeks_to_harvest"] = (
            p.get("weeks_from_transplant") or p.get("grow_time_weeks", 8)
            if start_type == "plant"
            else p.get("grow_time_weeks", 8)
        )
        if context in ("balcony", "garden"):
            enriched["overwinter"] = overwinter_assessment(p, location_zone)
        if optimistic:
            bd = enriched.get("score_breakdown", {})
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
            enriched["could_work_if"] = needs or ["conditions are close — try it"]
        return enriched

    TIMING_RANK = {"ok": 0, "tight": 1, "year_round": 0, "too_late": 2}

    def _sort_key(p):
        timing_rank = TIMING_RANK.get(p.get("timing", {}).get("status", "ok"), 2)
        weeks = p.get("weeks_to_harvest") or p.get("grow_time_weeks", 99)
        return (-p["match_score"], timing_rank, weeks)

    all_scored = sorted([_score_and_enrich(p) for p in candidates], key=_sort_key)
    qualified = [p for p in all_scored if p["match_score"] >= min_score]
    hidden = len(all_scored) - len(qualified)

    if shuffle and qualified:
        # Score-banded shuffle: plants within 0.05 of each other are equally good
        import random
        BAND = 0.05
        result = []
        i = 0
        while i < len(qualified):
            band_score = qualified[i]["match_score"]
            band = [p for p in qualified[i:] if band_score - p["match_score"] <= BAND]
            random.shuffle(band)
            result.extend(band)
            i += len(band)
        qualified = result

    # Draw from a pool wider than limit to give shuffle meaningful variation
    draw_pool = qualified[:max(pool, limit)]
    results = draw_pool[:limit]

    return {
        "results": results,
        "total_qualified": len(qualified),
        "hidden_weak": hidden,
        "empty_state": None if results else {
            "title": "No recommendations",
            "message": f"No plants passed the score threshold ({min_score}) for this location and conditions.",
            "suggestions": ["Lower min_score", "Try optimistic=true", "Try a different orientation"],
        },
    }


# ── Version helper ─────────────────────────────────────────────────────────────

def version_block() -> dict:
    return {
        "api_version": API_VERSION,
        "library_version": LIBRARY_VERSION,
        "scoring_version": SCORING_VERSION,
    }


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.get("/health")
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
    orientation: str = Query(..., pattern="^(N|NE|E|SE|S|SW|W|NW)$"),
    context: str = Query(..., pattern="^(windowsill|balcony|garden)$"),
    month: int = Query(default=0, ge=0, le=12),
    week: int | None = Query(default=None, ge=1, le=53),
    limit: int = Query(default=10, ge=1, le=50),
    min_score: float = Query(default=RELIABLE_THRESHOLD, ge=0.0, le=1.0),
    optimistic: bool = Query(default=False),
    shuffle: bool = Query(default=False),
    pool: int = Query(default=30, ge=1, le=145),
    exclude: str | None = Query(default=None),
    species: str | None = Query(default=None),
    type: str | None = Query(default=None),
    start_type: str = Query(default="seed", pattern="^(seed|plant)$"),
    response_format: str | None = Query(default=None, alias="format", pattern="^rima$"),
    _access: dict = Depends(require_access),
):
    if week is not None:
        m = week_to_month(week) if month == 0 else month
    else:
        m = month if month > 0 else datetime.now().month

    exclude_ids = [e.strip() for e in exclude.split(",")] if exclude else None

    climate_data = await fetch_all_monthly_temps(lat, lng)
    cond = await get_conditions(lat, lng, orientation, m, week, context)
    plants = load_plants()
    if climate_data and climate_data["months"]:
        winter_min = min(climate_data["months"].values())
    else:
        winter_min = coldest_month_temp(lat)
    scored = filter_and_score(plants, context, cond["avg_temp"], cond["sun_hours_direct"],
                              orientation, cond["data_confidence"], species, type,
                              start_type=start_type, lat=lat, month=m,
                              winter_min_temp=winter_min, week=week,
                              limit=limit, min_score=min_score, optimistic=optimistic,
                              shuffle=shuffle, pool=pool, exclude=exclude_ids)
    location_zone = usda_zone_from_temp(winter_min)
    zone_basis = "Open-Meteo archive" if (climate_data and climate_data["months"]) else "latitude estimate"
    payload = {
        **version_block(),
        "location": {"lat": lat, "lng": lng},
        "conditions": {**cond, "context": context},
        "location_zone": {"usda": location_zone, "basis": zone_basis},
        "start_type": start_type,
        "result_type": "estimated" if cond["data_confidence"] != "high" else "standard",
        "count": len(scored["results"]),
        "total_qualified": scored["total_qualified"],
        "hidden_weak": scored["hidden_weak"],
        "empty_state": scored["empty_state"],
        "recommendations": scored["results"],
    }
    if response_format == "rima":
        return rima_response(payload)
    return payload


@app.get("/v1/calendar")
async def calendar(
    lat: float = Query(..., ge=-90, le=90),
    lng: float = Query(..., ge=-180, le=180),
    orientation: str = Query(..., pattern="^(N|NE|E|SE|S|SW|W|NW)$"),
    context: str = Query(..., pattern="^(windowsill|balcony|garden)$"),
    limit: int = Query(default=3, ge=1, le=10),
    min_score: float = Query(default=RELIABLE_THRESHOLD, ge=0.0, le=1.0),
    optimistic: bool = Query(default=False),
    species: str | None = Query(default=None),
    type: str | None = Query(default=None),
    start_type: str = Query(default="seed", pattern="^(seed|plant)$"),
    _access: dict = Depends(require_access),
):
    plants = load_plants()
    climate_data = await fetch_all_monthly_temps(lat, lng)
    abs_lat = abs(lat)
    elevation = climate_data["elevation"] if climate_data else None

    winter_min = min(climate_data["months"].values()) if climate_data else coldest_month_temp(lat)

    months = []
    for m in range(1, 13):
        temp = climate_data["months"].get(m) if climate_data else None
        confidence = "high" if temp is not None else "low"
        if temp is None:
            temp = estimate_temp(lat, m)
        if elevation and elevation > 0:
            temp = round(temp - (elevation / 100) * 0.6, 1)
        m_adj = ((m - 1 + 6) % 12) + 1 if lat < 0 else m
        daylight = round(12 + math.sin(((m_adj - 3) / 12) * 2 * math.pi) * (abs_lat / 90 * 8), 1)
        sun = calc_sun_hours(lat, orientation, m, context)
        scored = filter_and_score(plants, context, temp, sun, orientation, confidence, species, type,
                                  start_type=start_type, lat=lat, month=m, winter_min_temp=winter_min,
                                  limit=limit, min_score=min_score, optimistic=optimistic)
        months.append({
            "month": m,
            "month_name": MONTH_NAMES[m],
            "avg_temp": temp,
            "sun_hours_direct": sun,
            "data_confidence": confidence,
            "recommendations": scored["results"],
        })

    overall = "high" if all(m["data_confidence"] == "high" for m in months) else "mixed"
    return {
        **version_block(),
        "location": {"lat": lat, "lng": lng, "elevation": elevation},
        "orientation": orientation,
        "context": context,
        "data_confidence": overall,
        "calendar": months,
    }


@app.get("/v1/conditions")
async def conditions(
    lat: float = Query(..., ge=-90, le=90),
    lng: float = Query(..., ge=-180, le=180),
    orientation: str = Query(..., pattern="^(N|NE|E|SE|S|SW|W|NW)$"),
    month: int = Query(default=0, ge=0, le=12),
    week: int | None = Query(default=None, ge=1, le=53),
    _access: dict = Depends(require_access),
):
    if week is not None:
        m = week_to_month(week) if month == 0 else month
    else:
        m = month if month > 0 else datetime.now().month
    cond = await get_conditions(lat, lng, orientation, m, week)
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


@app.get("/v1/now")
async def now(
    lat: float = Query(..., ge=-90, le=90),
    lng: float = Query(..., ge=-180, le=180),
    orientation: str = Query(..., pattern="^(N|NE|E|SE|S|SW|W|NW)$"),
    context: str = Query(..., pattern="^(windowsill|balcony|garden)$"),
    start_type: str = Query(default="seed", pattern="^(seed|plant)$"),
    optimistic: bool = Query(default=False),
    _access: dict = Depends(require_access),
):
    current_week = datetime.utcnow().isocalendar()[1]
    current_month = datetime.utcnow().month

    climate_data = await fetch_all_monthly_temps(lat, lng)
    cond = await get_conditions(lat, lng, orientation, current_month, current_week, context)
    plants = load_plants()
    winter_min = min(climate_data["months"].values()) if climate_data and climate_data["months"] else coldest_month_temp(lat)

    scored = filter_and_score(plants, context, cond["avg_temp"], cond["sun_hours_direct"],
                              orientation, cond["data_confidence"], None, None,
                              start_type=start_type, lat=lat, month=current_month,
                              winter_min_temp=winter_min, week=current_week,
                              limit=5, min_score=RELIABLE_THRESHOLD,
                              optimistic=optimistic, shuffle=True, pool=20)

    # what to harvest now — plants that are past their grow time
    harvest_now = [p for p in plants
                   if context in p.get("context", [])
                   and p.get("grow_time_weeks", 99) <= 4]

    # what needs attention — frost within 6 weeks
    frost_w = weeks_until_frost(lat, current_month, current_week)
    frost_warning = None
    if frost_w is not None and frost_w <= 6:
        frost_warning = f"Frost expected in ~{frost_w} weeks — move tender plants indoors or harvest now."

    return {
        **version_block(),
        "location": {"lat": lat, "lng": lng},
        "week": current_week,
        "week_label": week_label(current_week, current_month),
        "conditions": {**cond, "context": context},
        "plant_now": scored["results"],
        "watch_out": [w for w in [frost_warning] if w],
    }


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
