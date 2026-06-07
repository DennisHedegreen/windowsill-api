# Windowsill

Geo-climate edible plant growing recommendation API.

Send a GPS coordinate, a growing context, and a week number — get back the best plants to grow for that exact location, based on historical climate data and astronomical sun calculations.

**Live API:** https://api.windowsill.dk  
**Documentation:** https://windowsill.dk/docs.html  
**Plant library:** https://windowsill.dk/library.html  
**Contribute a plant:** https://windowsill.dk/contribute.html

Repository production library state: 148 varieties.
Merged research packs: 1 pending review.

Deployment note: verify `GET /v1/status` after deployment before claiming the live API has the same plant count.

---

## Quick start

No key required. 60 requests per hour per IP.

```bash
# What to plant this week
curl "https://api.windowsill.dk/v1/now?lat=55.67&lng=12.57&orientation=S&context=garden"

# Full recommendations by ISO week
curl "https://api.windowsill.dk/v1/recommend?lat=55.67&lng=12.57&orientation=S&context=garden&week=22"

# With shuffle — different top picks each call
curl "https://api.windowsill.dk/v1/recommend?lat=55.67&lng=12.57&orientation=SE&context=balcony&week=22&shuffle=true"

# Exclude plants you already have
curl "https://api.windowsill.dk/v1/recommend?lat=55.67&lng=12.57&orientation=S&context=garden&week=22&exclude=WSL-0001,WSL-0038"
```

Response:

```json
{
  "api_version": "0.6.0",
  "scoring_version": "0.8.0",
  "location": { "lat": 55.67, "lng": 12.57 },
  "conditions": {
    "week": 22,
    "week_label": "Week 22 (mid May)",
    "avg_temp": 14.1,
    "sun_hours_direct": 11.7,
    "elevation": 12.0,
    "orientation": "S"
  },
  "location_zone": { "usda": 8, "basis": "Open-Meteo archive" },
  "count": 10,
  "total_qualified": 38,
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
| `GET /v1/now` | What to plant this week — auto-detects current week |
| `GET /v1/recommend` | Ranked plant recommendations for a location and time |
| `GET /v1/calendar` | Top plants per month, full year view |
| `GET /v1/conditions` | Climate data for a location and time |
| `GET /v1/library` | Full plant library — repository currently contains 148 varieties |
| `GET /v1/varieties` | Filterable plant list |
| `GET /v1/varieties/{id}` | Single plant variety by ID |
| `GET /v1/health` | Service health |
| `GET /v1/status` | Plant count and cache status |

Full parameter reference: [REFERENCE.md](REFERENCE.md)

---

## Parameters — /v1/recommend

| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `lat` | yes | float | — | Latitude −90 to 90 |
| `lng` | yes | float | — | Longitude −180 to 180 |
| `orientation` | yes | enum | — | `N` `NE` `E` `SE` `S` `SW` `W` `NW` |
| `context` | yes | enum | — | `windowsill` `balcony` `garden` |
| `week` | no | integer | current week | ISO week 1–53. More precise than month. |
| `month` | no | integer | current month | 1–12. Used when `week` not supplied. |
| `limit` | no | integer | `10` | Max results returned (1–50) |
| `min_score` | no | float | `0.55` | Minimum match score (0.0–1.0) |
| `optimistic` | no | boolean | `false` | Relax temperature thresholds ±3°C |
| `shuffle` | no | boolean | `false` | Score-banded shuffle — vary results each call |
| `pool` | no | integer | `30` | Candidate pool size for shuffle |
| `exclude` | no | string | — | Comma-separated IDs to exclude, e.g. `WSL-0001,WSL-0038` |
| `start_type` | no | enum | `seed` | `seed` or `plant` — affects timing |
| `species` | no | string | — | Filter by species slug, e.g. `basil`, `tomato` |
| `type` | no | string | — | `op` `heirloom` `hybrid` |

---

## Authentication

```bash
# Header (preferred)
curl -H "X-API-Key: your-key" "https://api.windowsill.dk/v1/recommend?..."

# Query parameter
curl "https://api.windowsill.dk/v1/recommend?api_key=your-key&..."
```

Keys via email: api@windowsill.dk

Small non-commercial, educational, local, experimental or otherwise non-abusive projects can ask for a free key. The API is rate-limited to keep the service stable, not to turn small plant tools into a paywall.

See [docs/API_KEY_POLICY.md](docs/API_KEY_POLICY.md) for the working access policy.

| Plan | Limit |
|---|---|
| No key | 60 requests / hour per IP |
| Free | 1,000 requests / month |
| Builder | 10,000 requests / month |
| Sponsored | Unlimited |

---

## Plant library

148 edible plant varieties.

The original seeded library contained 145 varieties across four groups:

- Herbs and spices (85 varieties)
- Summer vegetables (25 varieties)
- Perennial garden herbs (20 varieties)
- Cold-tolerant / winter crops (15 varieties)

Additional release-candidate contributions currently include:

- Sacha Culantro
- Oca
- Ulluco

Each variety is one JSON file in `plants/`. IDs follow the format `WSL-0001`.

---

## Contribute a plant

The library is open.

New plants should start as research packs, not direct production plant files.

1. Fork this repository.
2. Create one folder under `research-packs/`.
3. Use the exact required files from `research-packs/_template/`.
4. Run `python3 scripts/validate_research_packs.py`.
5. Open a pull request and state that it is a research pack.

Do not update `plants/` or `plants/index.json` until a later review/promotion step accepts the plant for the production library.

AI-assisted contributions are welcome if they keep sources, uncertainty and human responsibility visible. See:

- [CONTRIBUTING.md](CONTRIBUTING.md)
- [docs/CHATGPT_PLANT_RESEARCH_GUIDE.md](docs/CHATGPT_PLANT_RESEARCH_GUIDE.md)
- [docs/RESEARCH_PACK_CONTRACT.md](docs/RESEARCH_PACK_CONTRACT.md)
- [docs/GITFLOW.md](docs/GITFLOW.md)
- [docs/WEEKLY_MERGE_PLAN.md](docs/WEEKLY_MERGE_PLAN.md)
- [docs/AI_PLANT_WORKFLOW.md](docs/AI_PLANT_WORKFLOW.md)
- [docs/SOURCE_HIERARCHY.md](docs/SOURCE_HIERARCHY.md)
- [docs/UNCERTAINTY_NOTES.md](docs/UNCERTAINTY_NOTES.md)
- [docs/PLANT_ENTRY_REVIEW.md](docs/PLANT_ENTRY_REVIEW.md)
- [research-packs/_template/](research-packs/_template/)

Research-pack pull requests are checked with:

```bash
python3 scripts/validate_research_packs.py
```

---

## No tracking

This API and its documentation site use no cookies and no analytics. Requests are logged at the infrastructure level only.

---

## Versions

| Version | Description |
|---|---|
| API v0.6.0 | Modern params: limit, min_score, optimistic, shuffle, exclude. New /v1/now endpoint. |
| API v0.5.0 | Context-aware sun model: balcony gets diffuse light from 3 sides, garden ignores orientation |
| API v0.4.0 | ISO week support, 8-point compass, elevation correction, real winter zones |
| Library 2026-06-07 | 148 repository varieties; verify live API after deployment |
| Scoring v0.8.0 | Score-banded shuffle, exclude filter, /v1/now |
| Scoring v0.7.0 | Context-aware sun hours in all scoring and calendar calculations |
| Scoring v0.6.0 | Week-precise frost timing, day-of-year sun calculation |

A Hedegreen Research project — api@windowsill.dk
