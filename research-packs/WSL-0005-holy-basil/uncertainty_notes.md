# Uncertainty notes — WSL-0005 Holy Basil

## High-level uncertainty

Holy Basil / Tulsi is a familiar plant, but it has more scope-boundary risk than ordinary sweet basil because many sources discuss it in spiritual, traditional and health-use contexts.

The Windowsill entry should stay narrow: edible plant / culinary and tea-style leaf use only.

## Estimated values

The following values are estimates:

- `species: "tenuiflorum"`
  - Used because `tenuiflorum` is the taxonomic species epithet in `Ocimum tenuiflorum`.
  - Existing `species: "basil"` is not taxonomic.

- `type: "op"`
  - Carried forward from the existing production entry.
  - Needs review if Windowsill treats the field as strict seed-line genetics.

- `min_temp: 18`
  - Practical active-growth threshold.
  - Not a survival threshold.

- `max_temp: 34`
  - Practical upper recommendation threshold for home/container growing.
  - Existing `40` is treated as too high for quality recommendation.

- `optimal_temp: 28`
  - Retained because Holy Basil is warmth-demanding.
  - Not a Holy-Basil-specific measured optimum.

- `sun_hours: 6`
  - Retained from the existing entry and supported by general basil guidance.

- `grow_time_weeks: 8`
  - Practical estimate for first realistic edible harvest from seed/sowing.

- `weeks_from_transplant: 4`
  - Practical estimate for first realistic edible harvest after transplanting or buying a young plant.

- `hardiness_temp: 0`
  - Used as a frost-boundary simplification.
  - Existing `-1` risks overstating cold tolerance.

- `hardiness_zone_min: 10`
  - Approximate warm-climate modelling value.

## Source disagreements

- Existing Windowsill production entry uses `Ocimum tenuiflorum`.
- Some sources and product labels use `Ocimum sanctum`.
- Some gardening sources warn that "holy basil" can be used loosely and may refer to different `Ocimum` species.
- General basil sources support light, frost sensitivity and container guidance, but are not Holy-Basil-specific trial data.
- Holy-Basil-specific home-gardening sources are useful but not formal expert review.

## Naming uncertainty

- Candidate pack value: `Ocimum tenuiflorum`.
- Known synonym/trade issue: `Ocimum sanctum`.
- This pack does not claim that every plant sold as Holy Basil or Tulsi is correctly labelled.
- Expert review should confirm preferred Latin name, synonym handling and whether Windowsill needs separate entries for different Tulsi types.

## Safety uncertainty

Low uncertainty for normal culinary/tea-style leaf use:

- Holy Basil leaves are used in food and tea contexts.

Boundary uncertainty:

- This entry covers normal food/tea-style use only.
- Supplements, extracts, essential oil, medicinal dosing and health claims are outside scope.
- Safety concerns connected to concentrated products or health-use contexts should not be imported into a simple edible-plant recommendation as if they were normal culinary use.

## Context uncertainty

### Windowsill

Included as acceptable, not ideal:

- Needs strong light.
- Needs warmth.
- Needs drainage.
- Needs airflow.
- Cool northern windowsills may underperform, especially in winter.

### Balcony

Included, but seasonal:

- Works best in warm, sunny, frost-free conditions.
- Small pots dry quickly.
- Wind and cold nights can damage plants.

### Garden

Included, but frost-free:

- Suitable during warm season.
- Not suitable for frost/cold periods.
- Treat as annual in temperate climates.

## Existing production fields that need human review

Existing entry reviewed from `plants/WSL-0005-holy-basil.json`:

- `species: "basil"`
  - Suggested correction: `tenuiflorum` if the field is taxonomic.

- `max_temp: 40`
  - Suggested correction: `34` as a practical recommendation threshold.

- `hardiness_temp: -1`
  - Suggested correction: `0`, with clear note that Holy Basil is frost-sensitive.

- `notes`
  - Suggested correction: keep cultural/Tulsi context, but do not imply health-use endorsement.

## Review recommendation

Mark this pack as:

`needs_human_check`

Do not mark as expert reviewed until three independent reviewers have actually assessed botanical name, edibility, container fit, climate fit and safety.
