"""API key authentication and a fixed window rate limiter."""
import math
import secrets
import time

from fastapi import Request, Response

from . import config
from .errors import ApiError

# API key -> (window number, requests used in that window)
_windows: dict[str, tuple[int, int]] = {}

WINDOW_SECONDS = 60


def reset_rate_limits() -> None:
    _windows.clear()


def _extract_key(request: Request) -> str:
    scheme, _, token = request.headers.get("authorization", "").partition(" ")
    if scheme.lower() != "bearer" or not token.strip():
        raise ApiError(
            401,
            "authentication_required",
            "Send your API key in the Authorization header as: Bearer YOUR_API_KEY.",
        )
    return token.strip()


def authenticate(request: Request, response: Response) -> str:
    key = _extract_key(request)
    if not any(secrets.compare_digest(key, valid) for valid in config.API_KEYS):
        raise ApiError(401, "invalid_api_key", "The API key is not valid.")

    limit = config.RATE_LIMIT_PER_MINUTE
    now = time.time()
    window = int(now // WINDOW_SECONDS)
    seconds_left = max(1, math.ceil((window + 1) * WINDOW_SECONDS - now))

    used_window, used = _windows.get(key, (window, 0))
    if used_window != window:
        used = 0
    if used >= limit:
        raise ApiError(
            429,
            "rate_limit_exceeded",
            f"You have used all {limit} requests for this minute. Retry in {seconds_left} seconds.",
            headers={
                "Retry-After": str(seconds_left),
                "X-RateLimit-Limit": str(limit),
                "X-RateLimit-Remaining": "0",
                "X-RateLimit-Reset": str(seconds_left),
            },
        )

    used += 1
    _windows[key] = (window, used)
    response.headers["X-RateLimit-Limit"] = str(limit)
    response.headers["X-RateLimit-Remaining"] = str(limit - used)
    response.headers["X-RateLimit-Reset"] = str(seconds_left)
    return key
