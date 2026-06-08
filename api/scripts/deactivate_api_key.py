#!/usr/bin/env python3
"""Deactivate a Windowsill API key by raw key or key hash.

Use this for exposed test keys or retired reviewer invitations.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "keys.db"


def hash_key(raw_key: str) -> str:
    return hashlib.sha256(raw_key.encode()).hexdigest()


@contextmanager
def sqlite_conn(path: Path):
    conn = sqlite3.connect(path)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def deactivate_sqlite(db_path: Path, key_hash: str) -> int:
    with sqlite_conn(db_path) as conn:
        cur = conn.execute("UPDATE api_keys SET active=0 WHERE key_hash=?", (key_hash,))
        conn.execute("UPDATE review_invitations SET active=0 WHERE key_hash=?", (key_hash,))
        return cur.rowcount


def deactivate_postgres(database_url: str, key_hash: str) -> int:
    try:
        import psycopg2
    except ImportError as exc:
        raise SystemExit("psycopg2 is required for DATABASE_URL key deactivation.") from exc

    conn = psycopg2.connect(database_url)
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE api_keys SET active=0 WHERE key_hash=%s", (key_hash,))
                rowcount = cur.rowcount
                cur.execute("UPDATE review_invitations SET active=0 WHERE key_hash=%s", (key_hash,))
                return rowcount
    finally:
        conn.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="Deactivate a Windowsill API key.")
    key_group = parser.add_mutually_exclusive_group(required=True)
    key_group.add_argument("--raw-key", help="Raw API key. It will be hashed before lookup.")
    key_group.add_argument("--key-hash", help="SHA-256 key hash.")
    parser.add_argument("--db", default=str(DB_PATH), help="SQLite keys.db path.")
    parser.add_argument("--use-database-url", action="store_true", help="Write to DATABASE_URL instead of local SQLite.")
    args = parser.parse_args()

    key_hash = args.key_hash or hash_key(args.raw_key)
    database_url = os.getenv("DATABASE_URL", "").strip()

    if args.use_database_url:
        if not database_url:
            raise SystemExit("--use-database-url requires DATABASE_URL.")
        changed = deactivate_postgres(database_url, key_hash)
        target = "DATABASE_URL"
    else:
        changed = deactivate_sqlite(Path(args.db), key_hash)
        target = args.db

    print(f"target: {target}")
    print(f"key_hash: {key_hash}")
    print(f"deactivated_api_keys: {changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
