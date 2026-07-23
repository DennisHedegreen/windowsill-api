# Uncertainty notes — WSL-0002 Thai Basil

## High-level uncertainty

Thai Basil is a familiar culinary herb, but the entry still has real audit uncertainty.

The biggest issue is not whether Thai basil leaves are normally used as food. The biggest issue is botanical naming and model compression: Windowsill has to compress cultivar/type identity, temperature response, indoor light, container fit, harvest timing and safety boundaries into one compact JSON object.

## Estimated values

The following values are estimates:

- `min_temp: 18`
  - Used as a practical lower active-growth threshold.
  - Not a survival threshold.
  - Thai basil may survive lower temperatures briefly, but cold will reduce performance.

- `max_temp: 34`
  - Used as a practical upper recommendation threshold before heat/water/quality stress becomes likely.
  - Not a death temperature.
  - Existing `38` may be possible survival heat, but it is too optimistic for a quality recommendation threshold.

- `optimal_temp: 27`
  - Model value inside the general basil optimal range supported by Rutgers.
  - Not a Thai-basil-specific measured optimum.

- `grow_time_weeks: 7`
  - Practical estimate for first realistic edible harvest from seed/sowing.
  - Supported weakly by Thai-basil-specific secondary guidance and generally by basil growth speed.
  - Needs human check if Windowsill wants conservative repeated-harvest timing.

- `weeks_from_transplant: 4`
  - Practical estimate for first realistic edible harvest after transplanting or buying a young plant.
  - Not directly proven by a strong Thai-basil-specific source in this pack.

- `hardiness_temp: 0`
  - Used only as frost boundary / survival-risk simplification.
  - Basil is frost-sensitive and should not be recommended for freezing conditions.

- `hardiness_zone_min: 10`
  - Approximate horticultural modelling value.
  - Thai basil is perennial only in warm/no-frost contexts and annual elsewhere.

- `type: "op"`
  - Carried forward from the existing production entry.
  - Not strongly confirmed by the sources in this pack.

## Source disagreements

- Kew POWO supports `Ocimum basilicum L.` as accepted species but does not list `var. thyrsiflora` among accepted infraspecifics.
- Iowa State Extension and The Spruce use `Ocimum basilicum var. thyrsiflora` for Thai basil.
- Some sources use spelling variants such as `thyrsiflora` and `thyrsiflorum`.
- General basil temperature sources may not apply perfectly to Thai basil.
- Thai-basil-specific sources often mix culinary, ornamental and home-gardening assumptions.
- Harvest timing sources vary between first leaves, first pruning, maturity and repeated harvest.

## Naming uncertainty

- Current production entry uses `Ocimum basilicum var. thyrsiflora`.
- Candidate pack keeps that label because it matches the existing entry and horticultural usage.
- Expert review should decide whether Windowsill should instead use:
  - `name_latin`: `Ocimum basilicum`
  - and treat Thai Basil as a cultivar/type label in notes.
- This pack does not claim that Thai Basil is a formally accepted infraspecific taxon under Kew POWO.
- This pack does not claim that Thai basil, holy basil and lemon basil are interchangeable.

## Safety uncertainty

Low uncertainty for normal culinary use:

- Leaves are commonly used as food.
- Tender stems may be used with leaves in normal culinary contexts.

Boundary uncertainty:

- This entry does not assess essential oil.
- This entry does not assess supplements.
- This entry does not assess extracts.
- This entry does not assess medicinal dosing.
- This entry does not assess pregnancy-specific safety.
- This entry does not assess allergy risk.
- BfR alkenylbenzene concerns apply as a caution around higher-exposure herb/spice/extract/supplement contexts, not as proof that ordinary Thai basil leaves are unsafe.

## Context uncertainty

### Windowsill

Included, but conditional:

- Needs strong light.
- Needs warmth.
- Needs drainage.
- Needs airflow.
- Indoor winter light may be insufficient in northern regions.
- Cold glass and drafts may stunt growth.

### Balcony

Included, but seasonal:

- Works best in warm, sunny, frost-free conditions.
- Small pots dry fast.
- Wind and cold nights can damage plants.
- Hot balconies may need extra water or some afternoon shade.

### Garden

Included, but frost-free:

- Suitable during warm season.
- Not suitable for frost/cold periods.
- Wet, crowded planting raises disease risk.
- Treat as annual in temperate climates.

## Existing production fields that need human review

Existing entry reviewed from `plants/WSL-0002-thai-basil.json`:

- `species: "basil"`
  - Suggested correction: `basilicum` if the field is taxonomic.

- `name_latin: "Ocimum basilicum var. thyrsiflora"`
  - Keep as candidate horticultural label, but botanical acceptance needs review.

- `max_temp: 38`
  - Suggested correction: `34` as practical active-growth quality threshold.

- `hardiness_temp: -1`
  - Suggested correction: `0`, with clear note that basil is frost-sensitive.

- `type: "op"`
  - Keep only provisionally unless seed-line source confirms it.

## Review recommendation

Mark this pack as:

`needs_human_check`

Do not mark as expert reviewed until three independent reviewers have actually assessed botanical name, edibility, container fit, climate fit and safety.
