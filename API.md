# Windowsill API

Current technical reference:

- `REFERENCE.md`

Live base URL:

- `https://api.windowsill.dk`

Current public API family:

- `GET /v1/now`
- `GET /v1/recommend`
- `GET /v1/calendar`
- `GET /v1/conditions`
- `GET /v1/library`
- `GET /v1/varieties`
- `GET /v1/varieties/{id}`
- `GET /v1/health`
- `GET /v1/status`

Current version block:

- API: `0.6.0`
- Library: `2026-06-07`
- Scoring: `0.8.0`

Do not use the older `mode=all/top10/optimal/optimistic` contract. Current recommendation clients should use `limit`, `min_score`, `optimistic`, `shuffle`, `pool`, `exclude`, `week`, `month`, `species`, `type`, `start_type`, and optional `format=compact`.

This file is kept as a short compatibility door because older local notes referenced `API.md`.
