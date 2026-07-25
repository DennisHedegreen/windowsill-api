# Windowsill Plant Preference Profile vNext

Status: workpack-only data contract
Updated: 2026-07-25

## Purpose

This contract lets Windowsill collect richer plant-preference data while the
current API remains unchanged.

It describes what a plant tends to like or avoid. It does **not** describe the
actual light, shade, weather, pot or watering state at a user's address.

In particular, this contract does not implement:

- a shade or indirect-light algorithm
- 3D buildings, trees, horizon or obstruction data
- a new API endpoint, response field or scoring factor
- a watering calculator or fixed millilitre-per-day advice

Those may later consume these preferences, but they are separate projects.

## Location

For each audited plant, store the profile at:

```text
research-packs/WSL-XXXX-name/vnext_profile.json
```

The file is required for new audit work started after this contract. Existing
packs are upgraded when they are worked on; do not bulk-fill unknown values.

## Data Rules

- `api_use` must stay `not_active` until a future explicit API contract.
- `status: source_ready` means the stated preferences have source support; it
  does not mean expert review or production promotion.
- Use `null` or `unknown` when evidence does not support a useful value.
- `source_refs` points to headings in the pack's `source_registry.md`.
- Do not turn a plant preference into a location calculation in this file.
- Do not store a fixed watering volume. Watering depends on the user's pot,
  substrate, weather, root size and actual light.
- Month-only planting advice is avoided. Establishment is captured relative to
  frost/season where a source supports it; a later local model can translate it
  into dates.

## Profile Shape v0

```json
{
  "schema_version": "windowsill.plant-preferences.v0",
  "status": "draft",
  "api_use": "not_active",
  "plant_id": "WSL-XXXX",
  "light": {
    "direct_sun_preference": "full_sun",
    "minimum_direct_sun_hours": null,
    "bright_indirect_tolerance": "unknown",
    "low_light_tolerance": "unknown",
    "supplemental_light": "unknown",
    "notes": ""
  },
  "container": {
    "container_suitable": "unknown",
    "minimum_volume_l": null,
    "preferred_volume_l": null,
    "minimum_depth_cm": null,
    "notes": ""
  },
  "water": {
    "moisture_preference": "unknown",
    "drought_tolerance": "unknown",
    "waterlogging_tolerance": "unknown",
    "guidance_style": "check_before_watering",
    "notes": ""
  },
  "establishment": {
    "indoor_start": "unknown",
    "direct_sow": "unknown",
    "transplant": "unknown",
    "month_guidance": "location_dependent",
    "notes": ""
  },
  "source_refs": {},
  "unknowns": []
}
```

### Controlled values

| Field | Values |
|---|---|
| `status` | `draft`, `source_ready`, `reviewed` |
| `light.direct_sun_preference` | `full_sun`, `part_sun`, `shade`, `unknown` |
| `light.bright_indirect_tolerance` | `good`, `conditional`, `not_suitable`, `unknown` |
| `light.low_light_tolerance` | `good`, `conditional`, `not_suitable`, `unknown` |
| `light.supplemental_light` | `may_help`, `not_needed`, `unknown` |
| `container.container_suitable` | `yes`, `conditional`, `no`, `unknown` |
| `water.moisture_preference` | `evenly_moist`, `allow_partial_dry`, `dry_between_waterings`, `unknown` |
| `water.drought_tolerance` | `low`, `medium`, `high`, `unknown` |
| `water.waterlogging_tolerance` | `low`, `medium`, `high`, `unknown` |
| `establishment.indoor_start` | `recommended`, `optional`, `not_recommended`, `unknown` |
| `establishment.direct_sow` | `after_frost`, `season_dependent`, `not_recommended`, `unknown` |
| `establishment.transplant` | `suitable`, `conditional`, `not_recommended`, `unknown` |

## Future Boundary

Later, a location/profile layer may combine these fields with a user's observed
light or future 3D shade model. That later layer must state its assumptions and
must not claim to observe conditions it has not measured.
