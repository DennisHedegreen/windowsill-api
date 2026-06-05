import hashlib
import sqlite3
import time
from pathlib import Path
from core.config import PLAN_LIMITS

DB_PATH = Path(__file__).parent.parent / "keys.db"


def _conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with _conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS api_keys (
                key_hash     TEXT PRIMARY KEY,
                owner        TEXT NOT NULL,
                project      TEXT,
                plan         TEXT NOT NULL DEFAULT 'free',
                monthly_limit INTEGER,
                usage_month  TEXT,
                usage_count  INTEGER NOT NULL DEFAULT 0,
                active       INTEGER NOT NULL DEFAULT 1,
                expires_at   INTEGER,
                note         TEXT,
                created_at   INTEGER NOT NULL
            )
        """)


def _hash(key: str) -> str:
    return hashlib.sha256(key.encode()).hexdigest()


def _current_month() -> str:
    return time.strftime("%Y-%m")


def lookup_key(raw_key: str) -> dict | None:
    h = _hash(raw_key)
    with _conn() as conn:
        row = conn.execute(
            "SELECT * FROM api_keys WHERE key_hash = ?", (h,)
        ).fetchone()
    if not row:
        return None
    return dict(row)


def check_and_increment(raw_key: str) -> tuple[bool, str]:
    """Returns (allowed, reason). Increments usage if allowed."""
    record = lookup_key(raw_key)
    if not record:
        return False, "invalid_key"
    if not record["active"]:
        return False, "key_inactive"
    if record["expires_at"] and time.time() > record["expires_at"]:
        return False, "key_expired"

    month = _current_month()
    limit = record["monthly_limit"]
    if limit is None:
        limit = PLAN_LIMITS.get(record["plan"])

    h = _hash(raw_key)
    with _conn() as conn:
        if record["usage_month"] != month:
            conn.execute(
                "UPDATE api_keys SET usage_month=?, usage_count=1 WHERE key_hash=?",
                (month, h)
            )
        else:
            if limit is not None and record["usage_count"] >= limit:
                return False, "monthly_limit_reached"
            conn.execute(
                "UPDATE api_keys SET usage_count=usage_count+1 WHERE key_hash=?",
                (h,)
            )
    return True, "ok"
