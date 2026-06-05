# Windowsill API — Technical Reference

Version: API v0.2.0 · Library 2026-06-05 · Scoring v0.5.0  
Base URL: https://windowsill-api-production.up.railway.app  
Documentation: https://windowsill.dk/docs.html  
Source: https://github.com/DennisHedegreen/windowsill-api

---

## Important

Windowsill gives growing recommendations, not guarantees. A `match_score` of 1.0 means the climate conditions match the plant's requirements — it does not account for local microclimate, soil quality, wind exposure, building shade, container size, watering practice, or pests. Use scores as a starting point, not a promise.

---

## Base URL

```
https://windowsill-api-production.up.railway.app
```

All endpoints accept `GET` requests. All responses are JSON.

Interactive API explorer: /docs  
Raw OpenAPI schema: /openapi.json

---

## Authentication

No key required for up to 60 requests per hour per IP.

```bash
# Header (preferred)
curl -H "X-API-Key: your-key" "https://windowsill-api-production.up.railway.app/v1/recommend?..."

# Query parameter
curl "https://windowsill-api-production.up.railway.app/v1/recommend?api_key=your-key&..."
```

Keys via email: api@windowsill.dk

| Plan | Limit | Key required |
|---|---|---|
| No key | 60 requests / hour per IP | No |
| Free | 1,000 requests / month | Yes |
| Builder | 10,000 requests / month | Yes |
| Sponsored | Unlimited | Yes |

### Rate limit headers

Every response includes:

| Header | Description |
|---|---|
| `X-RateLimit-Limit` | Requests allowed per hour |
| `X-RateLimit-Remaining` | Requests remaining this hour |
| `X-RateLimit-Reset` | Unix timestamp when limit resets |
| `Retry-After` | Seconds to wait (429 responses only) |

---

## Endpoints

### GET /v1/recommend

Ranked plant recommendations for a location and month.

**Parameters**

| Parameter | Required | Type | Description |
|---|---|---|---|
| `lat` | yes | float | Latitude −90 to 90 |
| `lng` | yes | float | Longitude −180 to 180 |
| `orientation` | yes | enum | `N` `S` `E` `W` — surface facing direction. Use closest cardinal direction. Diagonal orientations not currently supported. |
| `context` | yes | enum | `windowsill` `balcony` `garden` |
| `month` | no | integer | 1–12. Defaults to current month. |
| `mode` | no | enum | See mode table below. Default: `top10`. |
| `start_type` | no | enum | `seed` (default) `plant` — affects timing and weeks to harvest |
| `species` | no | string | Filter by species slug, e.g. `basil`, `tomato`, `kale` |
| `type` | no | string | Filter by variety type: `op` `heirloom` `hybrid` |

**Mode values**

| Mode | Description |
|---|---|
| `top10` | Up to 10 reliable matches (score ≥ 0.55). Default. |
| `optimal` | Single best reliable match only. |
| `optimistic` | Single stretch pick — uses relaxed temperature thresholds (±3°C). May include plants slightly outside their comfort zone. |
| `all` | Full ranked list including weak matches. For research and debugging. |

**Example**

```bash
curl "https://windowsill-api-production.up.railway.app/v1/recommend?lat=55.67&lng=12.57&orientation=S&context=garden&month=6&start_type=seed"
```

**Response fields**

| Field | Description |
|---|---|
| `api_version` | API version string |
| `library_version` | Plant library date |
| `scoring_version` | Scoring algorithm version |
| `location_zone.usda` | Estimated USDA hardiness zone for the location |
| `conditions` | Climate data used: avg temp, sun hours, orientation, data source |
| `count` | Number of results returned |
| `hidden_weak` | Number of matches below reliability threshold (not shown in top10/optimal) |
| `recommendations[]` | Ranked plant array |

**Per-plant fields**

| Field | Description |
|---|---|
| `match_score` | 0.0–1.0. Combined score for temperature, sun, habit, and safety. |
| `timing.status` | `ok` `tight` `too_late` `year_round` |
| `timing.note` | Human-readable timing with weeks to harvest and weeks to frost |
| `overwinter.status` | `yes` `marginal` `no` — balcony/garden only |
| `overwinter.plant_zone` | USDA zone required for the plant to overwinter |
| `weeks_to_harvest` | Weeks until first harvest from current start_type |
| `start_type` | The start_type used for this result |
| `score_breakdown` | Detailed scores per factor: temperature, sun, habit |
| `safety` | Present if plant has culinary safety flags |

---

### GET /v1/calendar

Best plant per month, full year view.

Same parameters as `/v1/recommend` except `month` is not accepted — returns all 12 months.

```bash
curl "https://windowsill-api-production.up.railway.app/v1/calendar?lat=55.67&lng=12.57&orientation=S&context=garden&mode=optimal"
```

Returns a `calendar` array with one entry per month. Each entry includes the best plant recommendation, avg temperature, and sun hours for that month.

---

### GET /v1/conditions

Climate data for a location and month, without plant recommendations.

| Field | Description |
|---|---|
| `avg_temp` | Average temperature for month (°C) |
| `sun_hours_direct` | Direct sun hours per day for the given orientation |
| `data_confidence` | `high` (Open-Meteo data) or `low` (latitude estimate) |
| `data_source` | Source description |

---

### GET /v1/library

Full plant library, optionally filtered by context.

```bash
curl "https://windowsill-api-production.up.railway.app/v1/library?context=windowsill"
```

---

### GET /v1/varieties

Filterable plant list. Filter by `species`, `type`, or `context`.

### GET /v1/varieties/{id}

Single plant variety by ID, e.g. `WSL-0001`.

### GET /v1/health

Service health, plant count, cache status.

### GET /v1/status

Plant count and climate cache size.

---

## Errors

| Status | Error code | Description |
|---|---|---|
| 400 | `invalid_parameters` | One or more query parameters are invalid |
| 401 | — | Invalid or expired API key |
| 404 | `not_found` | Endpoint or resource not found |
| 422 | `invalid_parameters` | Validation error — includes per-field details |
| 429 | — | Rate limit exceeded |
| 500 | `server_error` | Internal error |

**Validation error (422)**

```json
{
  "error": "invalid_parameters",
  "message": "One or more query parameters are invalid.",
  "details": [
    { "field": "lat", "error": "Input should be less than or equal to 90" }
  ]
}
```

**Rate limit (429)**

```json
{ "detail": "Rate limit reached (60 req/hour without key). Free API keys available." }
```

Headers: `Retry-After: 3600`

**Invalid key (401)**

```json
{ "detail": "Invalid API key." }
```

---

## Scoring model

### Windowsill

Indoors — outdoor temperature is irrelevant.

| Factor | Weight |
|---|---|
| Sun match | 0.60 |
| Habit (windowsill rating) | 0.40 |
| Temperature | not used |

### Balcony

Outdoor containers. Frost penalty applied when frost is less than 4 weeks away (max −0.30 to temperature score).

| Factor | Weight |
|---|---|
| Temperature match | 0.45 |
| Sun match | 0.35 |
| Habit (balcony rating) | 0.20 |

### Garden

Full outdoor exposure. Frost penalty applied when frost is less than 6 weeks away (max −0.40 to temperature score).

| Factor | Weight |
|---|---|
| Temperature match | 0.50 |
| Sun match | 0.30 |
| Habit (garden rating) | 0.20 |

### Temperature curve

Quadratic penalty from optimal temperature. Score drops to 0 below `min_temp` or above `max_temp`.

### Timing

Frost-hardy plants (`hardiness_temp ≤ −2°C`) are not blocked by frost — assessed on whether they can establish before frost arrives.

| Status | Meaning |
|---|---|
| `ok` | Enough time before frost to reach harvest |
| `tight` | Possible — start immediately |
| `too_late` | Not enough time before frost |
| `year_round` | No frost expected at this latitude |

---

## Plant schema

Each plant is one JSON file in `api/plants/`. IDs: `WSL-0001` format.

| Field | Type | Description |
|---|---|---|
| `id` | string | Unique ID — WSL-0001 format |
| `name_en` | string | English variety name |
| `name_da` | string | Danish variety name |
| `name_latin` | string | Latin/botanical name including cultivar |
| `family` | string | Botanical family |
| `genus` | string | Botanical genus |
| `species` | string | Common species slug, e.g. `basil` |
| `type` | enum | `op` `heirloom` `hybrid` |
| `min_temp` | float °C | Lowest temperature for active growth |
| `max_temp` | float °C | Highest temperature tolerated |
| `optimal_temp` | float °C | Optimal growing temperature |
| `hardiness_temp` | float °C | Coldest survival temperature (overwinter tolerance — distinct from min_temp) |
| `hardiness_zone_min` | integer | USDA zone derived from hardiness_temp |
| `sun_hours` | float | Minimum direct sun hours per day |
| `sun_direct` | enum | `full` `partial` `shade` |
| `context` | array | Suitable growing contexts |
| `grow_time_weeks` | integer | Weeks from seed to first harvest |
| `weeks_from_transplant` | integer | Weeks from transplant to first harvest |
| `habit` | object | Per-context suitability: `good` `acceptable` `risky` `unsuitable` |
| `notes` | string | Growing notes, culinary use, special requirements |

### min_temp vs hardiness_temp

`min_temp` is the temperature at which the plant stops growing.  
`hardiness_temp` is the temperature it can survive.

Example: Peppermint has `min_temp: 5°C` (stops growing in cold) but `hardiness_temp: −29°C` (survives winter as a dormant rhizome — USDA zone 5).

### USDA zone from hardiness_temp

| hardiness_temp | Zone |
|---|---|
| ≤ −34°C | 4 |
| −34 to −29°C | 5 |
| −29 to −23°C | 6 |
| −23 to −18°C | 7 |
| −18 to −12°C | 8 |
| −12 to −7°C | 9 |
| −7 to −1°C | 10 |
| −1 to +4°C | 11 |
| +4 to +10°C | 12 |
| > +10°C | 13 |

---

## Data sources

**Climate data:** Open-Meteo Archive API — global historical data 2003–2022. When unavailable, temperature is estimated from latitude (`data_confidence: low`).

**Sun calculation:** Astronomical calculation from latitude, orientation, and month. No external API.

**Plant library:** Maintained in this repository. Community contributions via pull request.

**USDA zones:** Estimated from latitude. Will be replaced with Open-Meteo winter data in a future version.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add a plant variety.

---

*Windowsill — Hedegreen Research — api@windowsill.dk*
