# Uncertainty notes — WSL-0001 Genovese Basil

## High-level uncertainty

This is a low-risk culinary herb entry, but it is not zero-uncertainty.

The main issue is not whether basil is edible. The main issue is modelling precision: Windowsill compresses cultivar identity, climate response, indoor light, harvest timing and safety boundaries into a small JSON object.

## Estimated values

The following values are estimates:

- `min_temp: 15`
  - Used as an active-growth threshold.
  - Not a survival threshold.
  - Basil can be damaged by cold/frost even if short exposures above/below this vary by plant condition.

- `max_temp: 32`
  - Based on the Rutgers/US Basil Consortium optimum range of 21–32°C.
  - Basil may survive or continue growing above this if watered and shaded, but heat stress risk rises.

- `optimal_temp: 26`
  - Model midpoint inside the cited optimum range.
  - Not a cultivar-specific measured optimum for Genovese Basil.

- `grow_time_weeks: 8`
  - A compromise between early leaf picking and full seed-to-harvest maturity.
  - Johnny's lists 68 days from seed; Kew notes earlier micro-herb use.

- `weeks_from_transplant: 5`
  - Based partly on Genovese-type transplant timing from seed-company data.
  - Needs human check if Windowsill wants standard Genovese rather than compact Everleaf-type timing.

- `hardiness_temp: 0`
  - Used only as a frost boundary / kill-risk simplification.
  - Basil is not frost hardy and should not be recommended for freezing conditions.

- `hardiness_zone_min: 10`
  - Approximate horticultural modelling value.
  - Basil is treated as annual in many temperate climates, so zone modelling is inherently awkward.

## Naming uncertainty

- Kew POWO supports `Ocimum basilicum L.` as the accepted species.
- `Ocimum basilicum 'Genovese'` is a practical horticultural label, but "Genovese" can mean cultivar, cultivar type, seed strain or region/DOP-associated production identity depending on source.
- Do not claim that all Genovese-labeled seeds are genetically identical.
- If Windowsill needs stricter taxonomy, consider a field split:
  - `name_latin`: `Ocimum basilicum`
  - `cultivar_or_type`: `Genovese`

## Edibility uncertainty

Low uncertainty for normal culinary use:

- Leaves are commonly eaten and supported by Kew.
- Flowers are also edible according to Kew.

Boundary uncertainty:

- This entry does not assess essential oil, supplements, extracts, medicinal use, pregnancy-specific use, high-dose use or allergy risk.
- BfR raises concern around alkenylbenzenes occurring in herbs such as basil and higher-exposure products such as pesto/extracts/supplements.

## Context uncertainty

### Windowsill

Included, but only with realistic conditions:

- Needs a sunny window or artificial light.
- Needs drainage and air circulation.
- Indoor winter light in northern Europe may be insufficient.

### Balcony

Included, with seasonal caution:

- Works in warm, sunny, frost-free conditions.
- Wind and cold nights can damage plants.

### Garden

Included, with frost and disease caution:

- Plant after frost risk.
- Avoid overcrowding/wet foliage because disease pressure rises.

## Fields from existing JSON that need human review

Existing entry reviewed from `plants/WSL-0001-genovese-basil.json`:

- `species: "basil"`
  - Suggested correction: `basilicum` if the field is taxonomic.

- `max_temp: 35`
  - Suggested correction: 32 as active-growth comfort maximum.

- `grow_time_weeks: 6`
  - Suggested correction: 8 as a safer first-useful-harvest model.

- `weeks_from_transplant: 3`
  - Suggested correction: 5.

- `hardiness_temp: -1`
  - Suggested correction: 0, with warning that basil is frost-sensitive and not happy near 0°C.

## Source disagreements or tension

- Seed suppliers vary on days to maturity and harvest readiness.
- Some sources discuss first edible leaves, others commercial harvest, others maturity.
- General basil sources may not apply perfectly to Genovese-specific strains.
- Indoor windowsill performance depends heavily on local light, glass orientation, season and room temperature.

## Review recommendation

Mark this pack as:

```text
needs_human_check
```

Do not mark as expert reviewed until three independent reviewers have actually assessed botanical name, edibility, container fit, climate fit and safety.
