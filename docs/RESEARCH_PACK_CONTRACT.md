# Windowsill Research Pack Contract

Status: operating contract
Updated: 2026-06-08

This contract defines the folder format for proposed plant additions.

Pull requests that add plant research packs should follow this structure before a plant is promoted into `plants/`.

## Folder shape

Use one folder per proposed plant:

```text
research-packs/WSL-XXXX-common-name/
```

Example:

```text
research-packs/WSL-XXXX-garden-cress/
```

Required files:

```text
plant.json
source_registry.md
field_rationale.md
uncertainty_notes.md
expert_review.md
pr_description.md
```

Do not put several plants in one pack.

Do not submit only a plant list.

## Plant JSON minimum

`plant.json` must be valid JSON and include these fields:

```text
id
contributor
contributor_note
name_en
name_latin
family
genus
species
type
min_temp
max_temp
optimal_temp
sun_hours
sun_direct
context
grow_time_weeks
weeks_from_transplant
hardiness_temp
hardiness_zone_min
habit
notes
expert_review
```

Allowed `sun_direct` values:

```text
full
partial
shade
```

Allowed `context` values:

```text
windowsill
balcony
garden
```

Allowed `habit` values for `windowsill`, `balcony`, and `garden`:

```text
good
acceptable
risky
unsuitable
unknown
```

## Field meaning lock

Do not add new plant timing or temperature fields until at least 10-20 new plant packs have been audited against the current schema.

These existing fields have fixed meanings:

| Field | Meaning |
|---|---|
| `grow_time_weeks` | Estimated weeks from seed/sowing to first realistic edible harvest. For herbs and cut crops, this means the first useful kitchen harvest, not biological maturity. |
| `weeks_from_transplant` | Estimated weeks from transplanting or buying a young plant to first realistic edible harvest. |
| `hardiness_temp` | Approximate survival threshold, not active growth temperature. This is used for overwinter tolerance and hardiness-zone reasoning. |
| `min_temp` | Practical lower threshold for active growth or realistic recommendation. Not the plant's survival minimum. |
| `optimal_temp` | Practical growth sweet spot. |
| `max_temp` | Practical upper threshold before heat stress or quality problems become likely. |

Do not add `maturity_weeks` to research packs yet.

If a future field is added after enough plants have been audited, `harvest_type` is the likely first candidate. For now, explain harvest behaviour in `field_rationale.md` and `notes`.

## Expert review field

Windowsill does not require expert review before a research pack can be submitted.

But the pack must reserve the field in the correct format.

Default state:

```json
{
  "expert_review": {
    "status": "not_reviewed",
    "model": "three_independent_reviewers_per_plant",
    "reviewers_required": 3,
    "reviews": [],
    "agreement_summary": {
      "botanical_name": "not_assessed",
      "edibility": "not_assessed",
      "container_fit": "not_assessed",
      "climate_fit": "not_assessed",
      "safety": "not_assessed"
    },
    "decision": "pending"
  }
}
```

The model means three independent plant-knowledge reviewers assess the same plant entry.

The point is not to force agreement.

The point is to make disagreement visible.

## Merge rule

A research pack can be merged when:

- the folder has all required files
- `plant.json` is valid JSON
- required fields are present
- values use the accepted controlled terms
- sources and uncertainty are not empty
- the pack does not claim expert review unless review notes exist

A plant should only be promoted into `plants/` after human review.

## Validator

Run locally:

```bash
python3 scripts/validate_research_packs.py
```

GitHub Actions runs the same validator on pull requests.
