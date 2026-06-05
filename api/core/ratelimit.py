import time
from collections import defaultdict
from core.config import RATE_LIMIT_NO_KEY

# Simple in-memory sliding window — good enough for single-instance v0.1
# Replace with Redis if multi-instance deploy is needed
_buckets: dict[str, list[float]] = defaultdict(list)
WINDOW = 3600  # 1 hour


def check_ip(ip: str) -> tuple[bool, int]:
    """Returns (allowed, requests_remaining)."""
    now = time.time()
    cutoff = now - WINDOW
    bucket = [t for t in _buckets[ip] if t > cutoff]
    _buckets[ip] = bucket

    if len(bucket) >= RATE_LIMIT_NO_KEY:
        return False, 0

    _buckets[ip].append(now)
    return True, RATE_LIMIT_NO_KEY - len(_buckets[ip])
