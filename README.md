# Windowsill

Geo-climate edible plant growing recommendation API.

Send a GPS coordinate, a growing context, and a month — get back the best plants to grow for that exact location, based on historical climate data and astronomical sun calculations.

**Live API:** https://windowsill-api-production.up.railway.app  
**Documentation:** https://windowsill.dk/docs.html  
**Contribute a plant:** https://windowsill.dk/contribute.html

---

## Quick start

No key required. 60 requests per hour per IP.

```bash
curl "https://windowsill-api-production.up.railway.app/v1/recommend?lat=55.67&lng=12.57&orientation=S&context=garden&month=6"
```

Response:

```json
{
  "api_version": "0.2.0",
  "scoring_version": "0.5.0",
  "location_zone": { "usda": 8 },
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
      "overwinter": {
        "status": "marginal",
        "plant_zone": 9
      }
    }
  ]
}
```

---

## Endpoints

| Endpoint | Description |
|---|---|
| `GET /v1/recommend` | Ranked plant recommendations for a location and month |
| `GET /v1/calendar` | Best plant per month, full year view |
| `GET /v1/conditions` | Climate data for a location and month |
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
| `orientation` | yes | enum | `N` `S` `E` `W` — surface facing direction |
| `context` | yes | enum | `windowsill` `balcony` `garden` |
| `month` | no | integer | 1–12. Defaults to current month. |
| `mode` | no | enum | `top10` (default) `optimal` `optimistic` `all` |
| `start_type` | no | enum | `seed` (default) `plant` |
| `species` | no | string | Filter by species slug, e.g. `basil`, `tomato` |
| `type` | no | string | `op` `heirloom` `hybrid` |

---

## Authentication

Pass key as header or query parameter:

```bash
# Header (preferred)
curl -H "X-API-Key: your-key" "https://windowsill-api-production.up.railway.app/v1/recommend?..."

# Query parameter
curl "https://windowsill-api-production.up.railway.app/v1/recommend?api_key=your-key&..."
```

Keys via email: api@windowsill.dk

| Plan | Limit |
|---|---|
| No key | 60 requests / hour per IP |
| Free | 1,000 requests / month |
| Builder | 10,000 requests / month |
| Sponsored | Unlimited |

Rate limit headers on every response: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`.

---

## Plant library

145 edible plant varieties across four groups:

- Herbs and spices (85 varieties)
- Summer vegetables (25 varieties)
- Perennial garden herbs (20 varieties)
- Cold-tolerant / winter crops (15 varieties)

Each variety is one JSON file in `api/plants/`. IDs follow the format `WSL-0001`.

---

## Contribute a plant

The library is open. To add a variety:

1. Fork this repository
2. Find the next available ID in `api/plants/` (currently WSL-0146+)
3. Create `api/plants/WSL-0146-your-plant-name.json` following the schema in [REFERENCE.md](REFERENCE.md#plant-schema)
4. Add the filename to `api/plants/index.json`
5. Open a pull request — include your data source in the description

---

## No tracking

This API and its documentation site use no cookies and no analytics. Requests are logged at the infrastructure level only.

---

## Versions

| Version | Description |
|---|---|
| API v0.2.0 | Current |
| Library 2026-06-05 | 145 varieties |
| Scoring v0.5.0 | Quadratic temp curve, frost-hardy timing, USDA zones |

A Hedegreen Research project — api@windowsill.dk
