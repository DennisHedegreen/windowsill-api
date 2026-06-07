import os

API_VERSION = "0.6.0"
LIBRARY_VERSION = "2026-06-07"
SCORING_VERSION = "0.8.0"

RELIABLE_THRESHOLD = 0.55
OPTIMISTIC_RANGE = (0.35, 0.68)

# CORS — locked to known origins in production
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

# Open-Meteo
CLIMATE_ARCHIVE_START = "2003-01-01"
CLIMATE_ARCHIVE_END = "2022-12-31"
CLIMATE_FETCH_TIMEOUT = 30

# Rate limiting (requests per hour per IP, no key)
RATE_LIMIT_NO_KEY = int(os.getenv("RATE_LIMIT_NO_KEY", "60"))

# API key plans: monthly request limits
PLAN_LIMITS = {
    "free": 1_000,
    "builder": 10_000,
    "pro": 100_000,
    "internal": None,       # no hard limit
    "sponsored": None,
}
