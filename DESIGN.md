# Windowsill — Design Document

## Concept

Windowsill is a geo-climate herb and vegetable growing recommendation API.

Send a GPS coordinate, a window orientation, and a growing context. Get back the best herb varieties to grow this month for that exact location — based on real historical climate data and astronomical sun calculations.

This is not a generic "herbs in June" list. It is a location-aware, orientation-aware, climate-backed recommendation engine.

---

## Input Parameters

| Parameter | Type | Description |
|---|---|---|
| `lat` | float | Latitude (GPS) |
| `lng` | float | Longitude (GPS) |
| `orientation` | string | Cardinal direction the surface faces: `N`, `S`, `E`, `W` |
| `context` | string | Growing environment: `windowsill`, `balcony`, `garden` |
| `month` | integer | Month number 1–12 (defaults to current month) |
| `start_type` | string | `seed` (default) or `plant` — affects timing and weeks_to_harvest |

---

## Output

A ranked list of herb variety recommendations with supporting climate data for the location and month.

```json
{
  "location": {
    "lat": 55.67,
    "lng": 12.57,
    "elevation": 10,
    "timezone": "Europe/Copenhagen"
  },
  "conditions": {
    "month": 6,
    "avg_temp": 16.4,
    "sun_hours_direct": 5.2,
    "orientation": "S",
    "context": "windowsill"
  },
  "recommendations": [
    {
      "id": "WSL-0001",
      "name_en": "Genovese Basil",
      "name_da": "Genovese Basilikum",
      "name_latin": "Ocimum basilicum 'Genovese'",
      "species": "basil",
      "type": "op",
      "match_score": 0.94,
      "notes": "Thrives in warm, sunny conditions. Ideal for south-facing windowsills."
    }
  ]
}
```

---

## Architecture

### Three data layers

**1. Astronomical sun calculation**
- Library: `pvlib` (Python)
- Input: lat/lng + orientation + month
- Output: daily direct sun hours for that surface
- No API calls — pure mathematics

**2. Historical climate data**
- Source: Open-Meteo Archive API (free, no key required)
- Coverage: global, daily data from 2000–2023
- Used to calculate monthly temperature normals per coordinate
- Cached per coordinate + month to avoid repeated calls

**3. Windowsill Plant Library**
- Maintained in this repository
- One record per variety (not per species)
- Curated manually — this is Windowsill's core contribution
- Open to community contributions via pull request
- 148 repository varieties
- Original seeded set: 145 varieties across four groups: herbs/spices, summer vegetables, perennial garden herbs, cold-tolerant/winter crops
- Current release-candidate additions: Sacha Culantro, Oca, Ulluco

---

## Plant Library Schema

Each herb variety is one record with the following fields:

| Field | Type | Description |
|---|---|---|
| `id` | string | Unique ID, format: `WSL-0001` |
| `contributor` | string | Name or GitHub handle of data contributor |
| `contributor_note` | string | Source or verification note |
| `name_en` | string | English variety name |
| `name_da` | string | Danish variety name |
| `name_latin` | string | Latin/botanical name (species + cultivar if applicable) |
| `family` | string | Botanical family (e.g. `Lamiaceae`) |
| `genus` | string | Botanical genus (e.g. `Ocimum`) |
| `species` | string | Common species grouping (e.g. `basil`, `mint`, `chive`) |
| `type` | string | `heirloom`, `hybrid`, or `op` (open-pollinated) |
| `min_temp` | float | Minimum temperature for growth (°C) |
| `max_temp` | float | Maximum temperature (°C) |
| `optimal_temp` | float | Optimal growing temperature (°C) |
| `sun_hours` | float | Minimum direct sun hours per day |
| `sun_direct` | string | `full`, `partial`, or `shade` |
| `context` | array | Suitable contexts: `windowsill`, `balcony`, `garden` |
| `grow_time_weeks` | integer | Weeks from sowing to first harvest |
| `weeks_from_transplant` | integer | Weeks from transplanting a young plant to first harvest |
| `hardiness_temp` | float | Coldest temperature the plant can survive (°C) — overwinter tolerance, not growth minimum |
| `hardiness_zone_min` | integer | USDA hardiness zone derived from `hardiness_temp` |
| `habit` | object | Per-context suitability: `windowsill`, `balcony`, `garden` — values: `good`, `acceptable`, `risky`, `unsuitable` |
| `notes` | string | Special requirements or observations |

### min_temp vs hardiness_temp

These are two distinct values that are often confused:

- `min_temp` — the lowest temperature at which the plant actively grows. Below this, growth stops.
- `hardiness_temp` — the lowest temperature the plant can survive (e.g. dormant underground, as a woody perennial, or as a self-seeding annual). This is what determines USDA hardiness zone.

Example: Peppermint has `min_temp: 5°C` (stops growing in cold) but `hardiness_temp: -29°C` (survives winter as a rhizome — USDA zone 5).

### Why variety-first, not species-first

Different varieties of the same species can have significantly different climate requirements. Genovese Basil and Thai Basil are not the same plant for growing purposes. Each variety gets its own record with its own climate data.

Filter by `species` to get all varieties of a given herb.

---

## Matching Algorithm

For a given location + month + orientation + context:

1. Calculate direct sun hours for the surface (astronomical)
2. Retrieve monthly temperature normal for the coordinate (Open-Meteo, cached)
3. Filter plant library by context
4. Score each variety against conditions (see Scoring per Context below)
5. Apply timing assessment based on `start_type` and weeks until frost
6. Return ranked list

Match score is 0.0–1.0. Only varieties above a minimum threshold are returned.

---

## Scoring per Context

Each context uses a different scoring model reflecting its real growing conditions.

### windowsill
Indoors — outdoor temperature is irrelevant.

| Factor | Weight |
|---|---|
| Sun | 0.60 |
| Habit (windowsill rating) | 0.40 |
| Temperature | not used |

### balcony
Outdoor containers — temperature matters, containers offer marginal cold protection.
Frost penalty applied when frost is < 4 weeks away (max −0.30 to t_score).

| Factor | Weight |
|---|---|
| Temperature | 0.45 |
| Sun | 0.35 |
| Habit (balcony rating) | 0.20 |

### garden
Full outdoor exposure — no container buffer. Frost cutoff is stricter than balcony.
Frost penalty applied when frost is < 6 weeks away (max −0.40 to t_score).

| Factor | Weight |
|---|---|
| Temperature | 0.50 |
| Sun | 0.30 |
| Habit (garden rating) | 0.20 |

---

## start_type and Timing

`start_type=seed` (default): uses `grow_time_weeks` to calculate weeks to harvest.
`start_type=plant`: uses `weeks_from_transplant` (shorter — assumes transplanting a young plant).

Each result includes a `timing` object:

| Status | Meaning |
|---|---|
| `ok` | Enough weeks before frost to reach harvest |
| `tight` | Possible but start immediately |
| `too_late` | Not enough time before frost |
| `year_round` | No frost risk at this latitude |

**Frost-hardy exception:** Plants with `hardiness_temp ≤ −2°C` are not blocked by frost. If frost is approaching but the plant can survive it, timing is assessed on whether the plant can establish before frost arrives — not on whether harvest happens before frost. This allows kale, mâche, leeks, mizuna and similar cold-season crops to show `ok` or `tight` in autumn rather than `too_late`.

---

## Hardiness Zones (USDA)

Each result for `balcony` and `garden` contexts includes an `overwinter` object indicating whether the plant can survive winter at the user's location.

### Location zone

Estimated from the coldest month minimum temperature, derived from latitude:

| Latitude range | Estimated winter min | USDA zone |
|---|---|---|
| ≥ 70° | −30°C | 4 |
| 60–70° | −18°C | 7 |
| 55–60° | −12°C | 8 |
| 50–55° | −7°C | 9 |
| 45–50° | −1°C | 10 |
| 40–45° | +5°C | 11 |
| 30–40° | +12°C | 12 |
| < 30° | +18–22°C | 12–13 |

When Open-Meteo winter temperature data is available for the coordinate, it will be used in preference to the latitude estimate (not yet implemented — currently always latitude-based).

### Overwinter assessment

| Status | Meaning |
|---|---|
| `yes` | Plant zone ≤ location zone — can overwinter outdoors |
| `marginal` | Plant zone = location zone + 1 — may survive mild winters with protection |
| `no` | Plant zone > location zone + 1 — annual only at this location |

Note: `no` does not mean the plant is unsuitable for the season — it simply means it will not survive winter outdoors and must be treated as an annual or brought indoors.

Overwinter assessment is only shown for `balcony` and `garden` contexts. It is not shown for `windowsill` (indoors, climate-controlled).

---

## Tech Stack

| Layer | Technology |
|---|---|
| API framework | Python / FastAPI |
| Sun calculation | pvlib |
| Climate data | Open-Meteo Archive API |
| Plant library | JSON (this repo) |
| Hosting | Railway |
| Caching | In-memory or Redis (TBD) |

---

## Growing Contexts

| Context | Description |
|---|---|
| `windowsill` | Indoor, protected, limited root space, controlled temperature |
| `balcony` | Outdoor, exposed to wind, variable temperature, containers |
| `garden` | Outdoor, ground or raised bed, full exposure |

More contexts may be added over time (e.g. `greenhouse`, `rooftop`).
