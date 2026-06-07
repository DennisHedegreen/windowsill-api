from fastapi import Request, HTTPException
from core.keys import check_and_increment
from core.ratelimit import check_ip


async def require_access(request: Request) -> dict:
    """FastAPI dependency. Returns access context dict."""
    raw_key = (
        request.headers.get("X-API-Key") or
        request.query_params.get("api_key")
    )

    if raw_key:
        allowed, reason = check_and_increment(raw_key)
        if not allowed:
            messages = {
                "invalid_key": "Invalid API key.",
                "key_inactive": "This API key has been deactivated.",
                "key_expired": "This API key has expired.",
                "monthly_limit_reached": "Monthly request limit reached. Email api@windowsill.dk for small-project or sponsored access.",
            }
            raise HTTPException(status_code=429 if "limit" in reason else 401,
                                detail=messages.get(reason, reason))
        return {"auth": "key", "key": raw_key}

    # No key — fall back to IP rate limiting
    ip = request.client.host if request.client else "unknown"
    allowed, remaining = check_ip(ip)
    if not allowed:
        raise HTTPException(
            status_code=429,
            detail=(
                "Rate limit reached. Add an API key for higher limits. "
                "Email api@windowsill.dk for a free small-project key."
            ),
            headers={"Retry-After": "3600"},
        )
    return {"auth": "ip", "ip": ip, "remaining": remaining}
