#!/usr/bin/env python3
"""Create a Windowsill API key and store only its hash.

Use this for manual keys after a reviewer or small project has been approved.
The raw key is printed once. Store/send it outside git.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import secrets
import sqlite3
import time
from contextlib import contextmanager
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "keys.db"
PLAN_LIMITS = {
    "free": 1_000,
    "builder": 10_000,
    "pro": 100_000,
    "internal": None,
    "sponsored": None,
}


def hash_key(raw_key: str) -> str:
    return hashlib.sha256(raw_key.encode()).hexdigest()


def generate_key(plan: str) -> str:
    return f"wsl_{plan}_{secrets.token_urlsafe(24)}"


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


def init_sqlite(conn: sqlite3.Connection) -> None:
    conn.execute("""
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
    conn.execute("""
        CREATE TABLE IF NOT EXISTS review_invitations (
            invite_id      TEXT PRIMARY KEY,
            key_hash       TEXT NOT NULL,
            reviewer_name  TEXT,
            reviewer_email TEXT,
            allowed_plants TEXT NOT NULL,
            active         INTEGER NOT NULL DEFAULT 1,
            created_at     INTEGER NOT NULL,
            note           TEXT
        )
    """)


def create_sqlite_key(args: argparse.Namespace, raw_key: str) -> None:
    created_at = int(time.time())
    with sqlite_conn(Path(args.db)) as conn:
        init_sqlite(conn)
        conn.execute(
            """
            INSERT INTO api_keys (
                key_hash, owner, project, plan, monthly_limit,
                usage_month, usage_count, active, expires_at, note, created_at
            )
            VALUES (?, ?, ?, ?, ?, NULL, 0, 1, ?, ?, ?)
            """,
            (
                hash_key(raw_key),
                args.owner,
                args.project,
                args.plan,
                args.monthly_limit,
                args.expires_at,
                args.note,
                created_at,
            ),
        )
        if args.review_plant:
            conn.execute(
                """
                INSERT INTO review_invitations (
                    invite_id, key_hash, reviewer_name, reviewer_email,
                    allowed_plants, active, created_at, note
                )
                VALUES (?, ?, ?, ?, ?, 1, ?, ?)
                """,
                (
                    args.invite_id or f"invite_{created_at}_{hash_key(raw_key)[:10]}",
                    hash_key(raw_key),
                    args.owner,
                    args.reviewer_email,
                    ",".join(args.review_plant),
                    created_at,
                    args.note,
                ),
            )


def create_postgres_key(args: argparse.Namespace, raw_key: str, database_url: str) -> None:
    try:
        import psycopg2
    except ImportError as exc:
        raise SystemExit("psycopg2 is required for DATABASE_URL key creation.") from exc

    conn = psycopg2.connect(database_url)
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
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
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS review_invitations (
                        invite_id      TEXT PRIMARY KEY,
                        key_hash       TEXT NOT NULL,
                        reviewer_name  TEXT,
                        reviewer_email TEXT,
                        allowed_plants TEXT NOT NULL,
                        active         INTEGER NOT NULL DEFAULT 1,
                        created_at     INTEGER NOT NULL,
                        note           TEXT
                    )
                """)
                created_at = int(time.time())
                cur.execute(
                    """
                    INSERT INTO api_keys (
                        key_hash, owner, project, plan, monthly_limit,
                        usage_month, usage_count, active, expires_at, note, created_at
                    )
                    VALUES (%s, %s, %s, %s, %s, NULL, 0, 1, %s, %s, %s)
                    """,
                    (
                        hash_key(raw_key),
                        args.owner,
                        args.project,
                        args.plan,
                        args.monthly_limit,
                        args.expires_at,
                        args.note,
                        created_at,
                    ),
                )
                if args.review_plant:
                    cur.execute(
                        """
                        INSERT INTO review_invitations (
                            invite_id, key_hash, reviewer_name, reviewer_email,
                            allowed_plants, active, created_at, note
                        )
                        VALUES (%s, %s, %s, %s, %s, 1, %s, %s)
                        """,
                        (
                            args.invite_id or f"invite_{created_at}_{hash_key(raw_key)[:10]}",
                            hash_key(raw_key),
                            args.owner,
                            args.reviewer_email,
                            ",".join(args.review_plant),
                            created_at,
                            args.note,
                        ),
                    )
    finally:
        conn.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a Windowsill API key.")
    parser.add_argument("--owner", required=True, help="Human owner or organization.")
    parser.add_argument("--project", default="", help="Project or use case.")
    parser.add_argument("--plan", default="free", choices=sorted(PLAN_LIMITS), help="API key plan.")
    parser.add_argument("--monthly-limit", type=int, default=None, help="Override monthly limit.")
    parser.add_argument("--expires-at", type=int, default=None, help="Unix timestamp expiry, optional.")
    parser.add_argument("--note", default="", help="Internal note.")
    parser.add_argument("--db", default=str(DB_PATH), help="SQLite keys.db path.")
    parser.add_argument("--use-database-url", action="store_true", help="Write to DATABASE_URL instead of local SQLite.")
    parser.add_argument("--review-plant", action="append", default=[], help="Plant ID this key may review. Repeat for multiple plants.")
    parser.add_argument("--reviewer-email", default="", help="Reviewer email for invitation metadata.")
    parser.add_argument("--invite-id", default="", help="Optional stable review invitation id.")
    args = parser.parse_args()

    raw_key = generate_key(args.plan)
    database_url = os.getenv("DATABASE_URL", "").strip()
    if args.use_database_url:
        if not database_url:
            raise SystemExit("--use-database-url requires DATABASE_URL.")
        create_postgres_key(args, raw_key, database_url)
        target = "DATABASE_URL"
    else:
        create_sqlite_key(args, raw_key)
        target = args.db

    print("Created Windowsill API key. Store the raw key outside git.")
    print(f"target: {target}")
    print(f"owner: {args.owner}")
    print(f"project: {args.project}")
    print(f"plan: {args.plan}")
    print(f"monthly_limit: {args.monthly_limit if args.monthly_limit is not None else PLAN_LIMITS[args.plan]}")
    if args.review_plant:
        print(f"review_plants: {','.join(args.review_plant)}")
    print(f"raw_key: {raw_key}")
    if args.review_plant:
        print(f"review_link: https://windowsill.dk/review/genovese-basil/?key={raw_key}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
