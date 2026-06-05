# Windowsill

Geo-climate edible plant growing recommendation API.

Send a GPS coordinate, a growing context, and a month or ISO week — get back the best plants to grow for that exact location, based on historical climate data and astronomical sun calculations.

**Live API:** https://api.windowsill.dk  
**Documentation:** https://windowsill.dk/docs.html  
**Contribute a plant:** https://windowsill.dk/contribute.html

---

## Quick start

No key required. 60 requests per hour per IP.

```bash
# By month
curl "https://api.windowsill.dk/v1/recommend?lat=55.67&lng=12.57&orientation=S&context=garden&month=6"

# By ISO week — more precise timing
curl "https://api.windowsill.dk/v1/recommend?lat=55.67&lng=12.57&orientation=SE&context=garden&week=22"
```

Response:

```json
{
  "api_version": "0.4.0",
  "scoring_version": "0.6.0",
  "location": { "lat": 55.67, "lng": 12.57 },
  "conditions": {
    "week": 22,
    "week_label": "Week 22 (mid May)",
    "avg_temp": 14.1,
    "sun_hours_direct": 11.7,
    "elevation": 12.0,
    "orientation": "SE"
  },
  "location_zone": { "usda": 8, "basis": "Open-Meteo archive" },
  "count": 10,
  "recommendations": [
    {
      "id": "WSL-0038",
      "name_en": "German Chamomile",
      "match_score": 1.0,
      "timing": {
        "status": "ok",
        "note": "Enough time — harvest expected ~4w, frost ~20w away."
      },
      "overwinter": { "status": "marginal", "plant_zone": 9 }
    }
  ]
}
```

---

## Endpoints

| Endpoint | Description |
|---|---|
| `GET /v1/recommend` | Ranked plant recommendations for a location and time |
| `GET /v1/calendar` | Best plant per month, full year view |
| `GET /v1/conditions` | Climate data for a location and time |
| `GET /v1/library` | Full plant library — 145 varieties |
| `GET /v1/varieties` | Filterable plant list |
| `GET /v1/varieties/{id}` | Single plant variety by ID |
| `GET /v1/health` | Service health |
| `GET /v1/status` | Plant count and cache status |

Full parameter reference: [REFERENCE.md](REFERENCE.md)

---

## Parameters — /v1/recommend

| Parameter | Required | Type | Description |
|---|---|---|---|
| `lat` | yes | float | Latitude −90 to 90 |
| `lng` | yes | float | Longitude −180 to 180 |
| `orientation` | yes | enum | `N` `NE` `E` `SE` `S` `SW` `W` `NW` — surface facing direction |
| `context` | yes | enum | `windowsill` `balcony` `garden` |
| `week` | no | integer | ISO week 1–53. Takes priority over `month`. More precise timing. |
| `month` | no | integer | 1–12. Defaults to current month. Used when `week` is not supplied. |
| `mode` | no | enum | `top10` (default) `optimal` `optimistic` `all` |
| `start_type` | no | enum | `seed` (default) `plant` — affects timing and weeks to harvest |
| `species` | no | string | Filter by species slug, e.g. `basil`, `tomato` |
| `type` | no | string | `op` `heirloom` `hybrid` |

---

## Authentication

```bash
# Header (preferred)
curl -H "X-API-Key: your-key" "https://api.windowsill.dk/v1/recommend?..."

# Query parameter
curl "https://api.windowsill.dk/v1/recommend?api_key=your-key&..."
```

Keys via email: api@windowsill.dk

| Plan | Limit |
|---|---|
| No key | 60 requests / hour per IP |
| Free | 1,000 requests / month |
| Builder | 10,000 requests / month |
| Sponsored | Unlimited |

---

## Plant library

145 edible plant varieties across four groups:

- Herbs and spices (85 varieties)
- Summer vegetables (25 varieties)
- Perennial garden herbs (20 varieties)
- Cold-tolerant / winter crops (15 varieties)

Each variety is one JSON file in `plants/`. IDs follow the format `WSL-0001`.

---

## Contribute a plant

The library is open. To add a variety:

1. Fork this repository
2. Find the next available ID in `plants/` (currently WSL-0146+)
3. Create `plants/WSL-0146-your-plant-name.json` following the schema in [REFERENCE.md](REFERENCE.md#plant-schema)
4. Add the filename to `plants/index.json`
5. Open a pull request — include your data source in the description

---

## No tracking

This API and its documentation site use no cookies and no analytics. Requests are logged at the infrastructure level only.

---

## Versions

| Version | Description |
|---|---|
| API v0.4.0 | ISO week support, 8-point compass, elevation correction, real winter zones |
| Library 2026-06-05 | 145 varieties |
| Scoring v0.6.0 | Week-precise frost timing, day-of-year sun calculation |

A Hedegreen Research project — api@windowsill.dk
