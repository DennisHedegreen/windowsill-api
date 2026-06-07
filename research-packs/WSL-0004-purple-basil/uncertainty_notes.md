# Uncertainty notes — WSL-0004 Purple Basil

## High-level uncertainty

Purple Basil is a normal culinary basil type, but the entry has naming uncertainty.

The key issue is that `Purple Basil` is a broad common-name/type-group label. The existing production file uses `Ocimum basilicum 'Purpurascens'`, but sources also discuss named cultivars such as `Dark Opal`, `Purple Ruffles`, `Red Rubin`, `Amethyst` and `Aromatto`.

## Estimated values

The following values are estimates:

- `name_latin: "Ocimum basilicum"`
  - Used as the safest species-level grounding.
  - Does not identify one exact purple cultivar.

- `species: "basilicum"`
  - Used because `basilicum` is the taxonomic species epithet.
  - Existing `species: "basil"` is not taxonomic.

- `type: "op"`
  - Carried forward from the existing production entry.
  - Needs review because Purple Basil is a broad type-group entry.

- `min_temp: 15`
  - Practical active-growth threshold.
  - Not a survival threshold.

- `max_temp: 33`
  - Practical upper recommendation threshold before heat and water stress become more likely.
  - Not a death temperature.

- `optimal_temp: 26`
  - Model value inside the general basil optimal range supported by Rutgers.
  - Existing `23` is likely too cool as the central sweet spot for warm-season basil.

- `sun_hours: 6`
  - Retained from the existing production entry.
  - Supported by general basil growing guidance.

- `grow_time_weeks: 7`
  - Practical estimate for first realistic edible harvest from seed/sowing.
  - Purple cultivars can vary.

- `weeks_from_transplant: 4`
  - Practical estimate for first realistic edible harvest after transplanting or buying a young plant.
  - Existing `3` may be possible for small early picking but is optimistic.

- `hardiness_temp: 0`
  - Used only as a frost-boundary simplification.
  - Basil should not be recommended for freezing conditions.

- `hardiness_zone_min: 10`
  - Approximate horticultural modelling value.
  - Purple Basil should be treated as annual in temperate climates.

## Source disagreements

- Existing Windowsill production entry uses `Ocimum basilicum 'Purpurascens'`.
- Kew POWO supports `Ocimum basilicum L.` at species level but does not verify a generic Purple Basil cultivar label.
- Iowa State treats purple-leaf basils as a group of cultivars.
- Horticultural sources use multiple purple-basil names, including `Dark Opal`, `Purple Ruffles`, `Red Rubin`, `Amethyst`, `Aromatto`, `Osmin Purple`, `purpureum` and `Purpurascens`.
- General basil sources support the climate model but are not Purple-Basil-specific trial data.

## Naming uncertainty

- Candidate pack value: `Ocimum basilicum`.
- Existing production value: `Ocimum basilicum 'Purpurascens'`.
- This pack does not claim that all Purple Basil is one cultivar.
- Expert review should decide whether Windowsill should keep a broad Purple Basil entry or split into cultivar-specific entries.

## Safety uncertainty

Low uncertainty for normal culinary use:

- Leaves are commonly used as food.
- Tender stems may be used with leaves in normal culinary contexts.

Boundary uncertainty:

- This entry covers normal culinary use only.
- Other uses are outside the scope of this pack.
- BfR-related caution is treated as a general basil/source-boundary note, not as evidence that ordinary Purple Basil leaves are unsafe.

## Context uncertainty

### Windowsill

Included, but conditional:

- Needs strong light.
- Needs warmth.
- Needs drainage.
- Needs airflow.
- Indoor winter light may be insufficient in northern regions.
- Weak light may reduce purple colour quality.

### Balcony

Included, but seasonal:

- Works best in warm, sunny, frost-free conditions.
- Small pots dry quickly.
- Wind and cold nights can damage plants.
- Hot balconies may need extra water or some afternoon shade.

### Garden

Included, but frost-free:

- Suitable during warm season.
- Not suitable for frost/cold periods.
- Wet, crowded planting raises disease risk.
- Treat as annual in temperate climates.

## Existing production fields that need human review

Existing entry reviewed from `plants/WSL-0004-purple-basil.json`:

- `name_latin: "Ocimum basilicum 'Purpurascens'"`
  - Suggested review: consider `Ocimum basilicum` for a broad type-group entry, or split into named cultivars.

- `species: "basil"`
  - Suggested correction: `basilicum` if the field is taxonomic.

- `optimal_temp: 23`
  - Suggested correction: `26` as practical warm-season sweet spot.

- `max_temp: 34`
  - Suggested correction: `33` as practical upper recommendation value.

- `weeks_from_transplant: 3`
  - Suggested correction: `4`.

- `hardiness_temp: -1`
  - Suggested correction: `0`, with clear note that basil is frost-sensitive.

## Review recommendation

Mark this pack as:

`needs_human_check`

Do not mark as expert reviewed until three independent reviewers have actually assessed botanical name, edibility, container fit, climate fit and safety.
