# Windowsill API

Geo-climate edible plant growing recommendation API.

Send a GPS coordinate, a growing context, and a month — get back the best edible plants to grow for that exact location, based on historical climate data and astronomical sun calculations.

## Endpoints

```
GET /v1/recommend   — ranked plant recommendations
GET /v1/calendar    — best plant per month, full year
GET /v1/conditions  — climate data for a location and month
GET /v1/library     — full plant library (145 varieties)
GET /v1/varieties   — filterable plant list
GET /v1/health      — service health
```

## Quick start

```bash
curl "https://your-railway-url/v1/recommend?lat=55.67&lng=12.57&orientation=S&context=garden&month=6"
```

## Parameters

| Parameter | Required | Values |
|---|---|---|
| `lat` | yes | −90 to 90 |
| `lng` | yes | −180 to 180 |
| `orientation` | yes | `N`, `S`, `E`, `W` |
| `context` | yes | `windowsill`, `balcony`, `garden` |
| `month` | no | 1–12 (default: current month) |
| `mode` | no | `top10`, `optimal`, `optimistic`, `all` |
| `start_type` | no | `seed` (default), `plant` |

## Access

- No key: 60 requests/hour per IP
- Free key: 1,000 requests/month
- Contact: windowsill@hedegreenresearch.com

## Deploy

Railway — see `api/railway.toml`. Set `DATABASE_URL` (Postgres) and optionally `CORS_ORIGINS`.
