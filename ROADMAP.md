# Windowsill — Roadmap

Updated: 2026-06-07

## Done

**Phase 1 — Foundation**
- [x] Plant library JSON schema
- [x] Plant library seeded — 145 original varieties
- [x] Plant library expanded in repository — 148 varieties
- [x] Astronomical sun calculation
- [x] Open-Meteo climate data fetching + caching
- [x] Matching algorithm (temp + sun score)
- [x] FastAPI endpoints
- [x] Deployed to Railway
- [x] Public API documentation at windowsill.dk
- [x] CONTRIBUTING.md with schema and verification guidelines
- [x] AI-assisted plant contribution workflow
- [x] Source hierarchy / uncertainty / review direction documented locally
- [x] GitHub-based contribution flow (PR per variety)
- [x] Credit system (contributor field in API response)
- [x] Heirloom and open-pollinated focus
- [x] Stable versioned API (`/v1/`)
- [x] Rate limiting and API keys

**Phase 2 — Precision**
- [x] 8-point compass orientation (N/NE/E/SE/S/SW/W/NW)
- [x] Elevation correction (−0.6°C/100m from Open-Meteo)
- [x] Real winter temperature data for USDA zone (Open-Meteo archive, was latitude estimate)
- [x] ISO week parameter — weekly temperature averages, day-of-year sun calculation
- [x] Custom domain: api.windowsill.dk

---

## Next

**Phase 3 — Context & Timing**

- [ ] Frost date calculation per coordinate from Open-Meteo data (currently latitude estimate)
- [ ] Growing season start/end per location
- [ ] `/v1/calendar` with week resolution (currently month-only)
- [ ] Sowing schedule — when to start indoors vs direct sow

**Phase 4 — Language**

- [ ] `lang=da` parameter — Danish names and notes in response
- [ ] Danish variety names already in library — just needs routing

**Phase 5 — Ecosystem**

- [ ] SDKs or code examples (Python, JavaScript)
- [ ] Public plant library as standalone downloadable dataset
- [ ] Companion planting recommendations
- [ ] Rate limiting dashboard for API key holders

**Phase 6 — Trust Layers**

- [x] API key access policy drafted locally
- [ ] Taxonomic Review Score design implemented as data fields or linked review records
- [ ] Community Signal design implemented as separate field reports
- [ ] Phone-first contribution path via issue/discussion templates
- [ ] Public disagreement display for disputed plant fields
- [ ] Plant entry review templates connected to contribution flow

---

## TID Tool

- [x] Windowsill tool source exists locally — 3-screen flow (input -> results -> report/PDF)
- [x] Register Windowsill in Hedegreen Research TID objects
- [x] Build/stage/upload public TID route
- [x] Windowsill BUILD article published on Hedegreen Research
- [x] Heat Pressure: live Windowsill API call for Rima household prompt

Live surfaces:

- TID tool: https://hedegreenresearch.com/tid/windowsill/tool/
- BUILD article: https://hedegreenresearch.com/articles/the-window-became-a-climate-interface/

---

## App

- [ ] Android app — compass + GPS → instant recommendation (Flutter, planned)
