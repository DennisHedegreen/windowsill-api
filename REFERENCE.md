# Windowsill API — Technical Reference

Version: API v0.5.0 · Library 2026-06-05 · Scoring v0.7.0  
Base URL: https://api.windowsill.dk  
Documentation: https://windowsill.dk/docs.html  
Source: https://github.com/DennisHedegreen/windowsill-api

---

## Important

Windowsill gives growing recommendations, not guarantees. A `match_score` of 1.0 means the climate conditions match the plant's requirements — it does not account for local microclimate, soil quality, wind exposure, building shade, container size, watering practice, or pests. Use scores as a starting point, not a promise.

---

## Base URL

```
https://api.windowsill.dk
```

All endpoints accept `GET` requests. All responses are JSON.

Interactive API explorer: /docs  
Raw OpenAPI schema: /openapi.json

---

## Authentication

No key required for up to 60 requests per hour per IP.

```bash
# Header (preferred)
curl -H "X-API-Key: your-key" "https://api.windowsill.dk/v1/recommend?..."

# Query parameter
curl "https://api.windowsill.dk/v1/recommend?api_key=your-key&..."
```

Keys via email: api@windowsill.dk

| Plan | Limit | Key required |
|---|---|---|
| No key | 60 requests / hour per IP | No |
| Free | 1,000 requests / month | Yes |
| Builder | 10,000 requests / month | Yes |
| Sponsored | Unlimited | Yes |

### Rate limit headers

| Header | Description |
|---|---|
| `X-RateLimit-Limit` | Requests allowed per hour |
| `X-RateLimit-Remaining` | Requests remaining this hour |
| `X-RateLimit-Reset` | Unix timestamp when limit resets |
| `Retry-After` | Seconds to wait (429 responses only) |

---

## Endpoints

### GET /v1/recommend

Ranked plant recommendations for a location and time.

**Parameters**

| Parameter | Required | Type | Description |
|---|---|---|---|
| `lat` | yes | float | Latitude −90 to 90 |
| `lng` | yes | float | Longitude −180 to 180 |
| `orientation` | yes | enum | `N` `NE` `E` `SE` `S` `SW` `W` `NW` — surface facing direction |
| `context` | yes | enum | `windowsill` `balcony` `garden` |
| `week` | no | integer | ISO week 1–53. Takes priority over `month`. Uses weekly temperature averages and day-of-year sun calculation for higher precision. |
| `month` | no | integer | 1–12. Defaults to current month. Used when `week` is not supplied. |
| `mode` | no | enum | See mode table below. Default: `top10`. |
| `start_type` | no | enum | `seed` (default) `plant` — affects timing and weeks to harvest |
| `species` | no | string | Filter by species slug, e.g. `basil`, `tomato`, `kale` |
| `type` | no | string | Filter by variety type: `op` `heirloom` `hybrid` |

**Mode values**

| Mode | Description |
|---|---|
| `top10` | Up to 10 reliable matches (score ≥ 0.55). Default. |
| `optimal` | Single best reliable match only. |
| `optimistic` | Single stretch pick — relaxed temperature thresholds (±3°C). |
| `all` | Full ranked list including weak matches. |

**Examples**

```bash
# By month
curl "https://api.windowsill.dk/v1/recommend?lat=55.67&lng=12.57&orientation=S&context=garden&month=6&start_type=seed"

# By ISO week — more precise
curl "https://api.windowsill.dk/v1/recommend?lat=55.67&lng=12.57&orientation=SE&context=balcony&week=22"
```

**Response fields**

| Field | Description |
|---|---|
| `api_version` | API version string |
| `library_version` | Plant library date |
| `scoring_version` | Scoring algorithm version |
| `location_zone.usda` | USDA hardiness zone — from Open-Meteo winter data when available |
| `location_zone.basis` | `Open-Meteo archive` or `latitude estimate` |
| `conditions` | Climate data used for scoring |
| `conditions.week` | ISO week number (when `week` parameter was used) |
| `conditions.week_label` | Human label, e.g. `Week 22 (mid May)` |
| `conditions.elevation` | Elevation in metres from Open-Meteo |
| `conditions.avg_temp` | Average temperature (°C), elevation-corrected |
| `conditions.sun_hours_direct` | Effective sun hours — adjusted for context (see Sun model below) |
| `count` | Number of results returned |
| `hidden_weak` | Matches below reliability threshold (hidden in top10/optimal) |
| `recommendations[]` | Ranked plant array |

**Per-plant fields**

| Field | Description |
|---|---|
| `match_score` | 0.0–1.0. Combined score for temperature, sun, habit, and safety. |
| `timing.status` | `ok` `tight` `too_late` `year_round` |
| `timing.note` | Timing detail with weeks to harvest and weeks to frost |
| `overwinter.status` | `yes` `marginal` `no` — balcony/garden only |
| `overwinter.plant_zone` | USDA zone required for the plant to overwinter |
| `weeks_to_harvest` | Weeks until first harvest from current start_type |
| `score_breakdown` | Scores per factor: temperature, sun, habit |
| `safety` | Present if plant has culinary safety flags |

---

### GET /v1/calendar

Best plant per month, full year view.

Same parameters as `/v1/recommend` except `month` and `week` — returns all 12 months. Elevation correction applied to all months.

```bash
curl "https://api.windowsill.dk/v1/calendar?lat=55.67&lng=12.57&orientation=S&context=garden&mode=optimal"
```

---

### GET /v1/conditions

Climate data for a location and time, without plant recommendations.

| Parameter | Description |
|---|---|
| `lat`, `lng` | Required |
| `orientation` | Required — `N` `NE` `E` `SE` `S` `SW` `W` `NW` |
| `week` | Optional ISO week. More precise than month. |
| `month` | Optional. Used when week not supplied. |

| Response field | Description |
|---|---|
| `avg_temp` | Average temperature (°C), elevation-corrected |
| `sun_hours_direct` | Direct sun hours per day for the given orientation |
| `sun_hours_total` | Total daylight hours |
| `elevation` | Metres above sea level from Open-Meteo |
| `week` | ISO week (when supplied) |
| `week_label` | Human label, e.g. `Week 22 (mid May)` |
| `data_confidence` | `high` (Open-Meteo) or `low` (latitude estimate) |
| `data_source` | Source description |

---

### GET /v1/library

Full plant library, optionally filtered by context.

```bash
curl "https://api.windowsill.dk/v1/library?context=windowsill"
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
| 422 | `invalid_parameters` | Validation error — includes per-field details |
| 401 | — | Invalid or expired API key |
| 404 | `not_found` | Endpoint or resource not found |
| 429 | — | Rate limit exceeded |
| 500 | `server_error` | Internal error |

---

## Scoring model

### Windowsill

Indoors — outdoor temperature not used.

| Factor | Weight |
|---|---|
| Sun match | 0.60 |
| Habit (windowsill rating) | 0.40 |

### Balcony

Outdoor containers. Frost penalty when frost < 4 weeks away (max −0.30).

| Factor | Weight |
|---|---|
| Temperature match | 0.45 |
| Sun match | 0.35 |
| Habit (balcony rating) | 0.20 |

### Garden

Full outdoor. Frost penalty when frost < 6 weeks away (max −0.40).

| Factor | Weight |
|---|---|
| Temperature match | 0.50 |
| Sun match | 0.30 |
| Habit (garden rating) | 0.20 |

### Sun model — context-aware calculation

Sun hours are not a simple orientation lookup. The calculation depends on context:

**Windowsill** — one face only. Direct sun from the chosen orientation.

| Orientation (northern hemisphere) | Factor |
|---|---|
| S | 0.70 |
| SE / SW | 0.55 |
| E / W | 0.40 |
| NE / NW | 0.25 |
| N | 0.10 |

**Balcony** — open on three sides. Primary face contributes 60%, each neighbouring direction 20%. A N-facing balcony still receives diffuse light from NW and NE.

```
sun = daylight × (primary × 0.60 + left_neighbour × 0.20 + right_neighbour × 0.20)
```

Example — N-facing balcony, Copenhagen, week 22:  
`daylight × (0.10 × 0.60 + 0.55 × 0.20 + 0.55 × 0.20) = daylight × 0.28`

**Garden** — open sky. Orientation is ignored. Garden plots receive approximately 85% of full daylight (terrain and tree margin).

```
sun = daylight × 0.85
```

### Orientation quality factors

| Orientation | Quality |
|---|---|
| S | 1.00 |
| SE / SW | 0.90 |
| E / W | 0.75 |
| NE / NW | 0.50 |
| N | 0.35 |

### Timing

Week-precise when `week` parameter is used. Frost-hardy plants (`hardiness_temp ≤ −2°C`) assessed on establishment time, not harvest-before-frost.

| Status | Meaning |
|---|---|
| `ok` | Enough time before frost |
| `tight` | Possible — start immediately |
| `too_late` | Not enough time before frost |
| `year_round` | No frost expected |

### Elevation correction

Temperature is corrected for elevation using the standard lapse rate: **−0.6°C per 100 metres**. Elevation is taken from the Open-Meteo archive response for the coordinate.

---

## Plant schema

Each plant is one JSON file in `plants/`. IDs: `WSL-0001` format.

| Field | Type | Description |
|---|---|---|
| `id` | string | Unique ID — WSL-0001 format |
| `name_en` | string | English variety name |
| `name_da` | string | Danish variety name |
| `name_latin` | string | Latin/botanical name including cultivar |
| `family` | string | Botanical family |
| `genus` | string | Botanical genus |
| `species` | string | Species slug, e.g. `basil` |
| `type` | enum | `op` `heirloom` `hybrid` |
| `min_temp` | float °C | Lowest temperature for active growth |
| `max_temp` | float °C | Highest temperature tolerated |
| `optimal_temp` | float °C | Optimal growing temperature |
| `hardiness_temp` | float °C | Coldest survival temperature |
| `hardiness_zone_min` | integer | USDA zone derived from hardiness_temp |
| `sun_hours` | float | Minimum direct sun hours per day |
| `sun_direct` | enum | `full` `partial` `shade` |
| `context` | array | Suitable contexts: `windowsill` `balcony` `garden` |
| `grow_time_weeks` | integer | Weeks from seed to first harvest |
| `weeks_from_transplant` | integer | Weeks from transplant to first harvest |
| `habit` | object | Per-context suitability: `good` `acceptable` `risky` `unsuitable` |
| `notes` | string | Growing notes and special requirements |

### min_temp vs hardiness_temp

`min_temp` — temperature at which growth stops.  
`hardiness_temp` — lowest temperature the plant survives.

Example: Peppermint `min_temp: 5°C`, `hardiness_temp: −29°C` — stops growing in cold but survives winter as a dormant rhizome.

---

## Data sources

| Source | Used for |
|---|---|
| Open-Meteo Archive API | Monthly and weekly temperature averages 2003–2022. Elevation. Winter minimum for USDA zone. |
| Astronomical calculation | Sun hours from latitude, orientation, day of year, and growing context. No external API. |
| Plant library | Maintained in this repository. Community contributions via pull request. |

When Open-Meteo is unavailable, temperature is estimated from latitude (`data_confidence: low`).

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add a plant variety.

---

*Windowsill — Hedegreen Research — api@windowsill.dk*
