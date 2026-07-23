# Field rationale — WSL-0004 Purple Basil

## Summary

This is an audit pack for the existing Windowsill plant entry `plants/WSL-0004-purple-basil.json`.

The existing entry is broadly plausible, but several fields need human review:

- The current `name_latin` value, `Ocimum basilicum 'Purpurascens'`, may be too specific for a broad Purple Basil entry.
- `species: "basil"` should be `basilicum` if the field is taxonomic.
- `optimal_temp: 23` is probably too cool as the main growth sweet spot for a warm-season basil.
- `weeks_from_transplant: 3` is optimistic for a useful culinary harvest.
- `hardiness_temp: -1` risks implying more cold tolerance than basil normally has.

## Botanical identity

Candidate value:

- `name_latin`: `Ocimum basilicum`

Rationale:

- Kew POWO supports `Ocimum basilicum L.` as an accepted species.
- Iowa State Extension describes purple-leaf basils as a group of culinary and ornamental basil cultivars.
- Purple Basil is treated here as a type-group entry, not one verified cultivar.
- The production value `Ocimum basilicum 'Purpurascens'` may still be useful, but it needs review before it is treated as the best name.

Uncertainty:

- Purple Basil may refer to several cultivars, including `Dark Opal`, `Purple Ruffles`, `Red Rubin`, `Amethyst` and `Aromatto`.
- This pack should not claim that all purple basil seed is one identical cultivar.

## Family / genus / species

Candidate values:

- `family`: `Lamiaceae`
- `genus`: `Ocimum`
- `species`: `basilicum`

Rationale:

- Kew POWO supports `Ocimum basilicum` in `Lamiaceae` and genus `Ocimum`.
- `species: "basil"` is not a taxonomic species epithet.

## Type

Candidate value:

- `type`: `op`

Rationale:

- The existing production entry uses `op`.
- This value is carried forward provisionally.

Uncertainty:

- Purple Basil is a broad type-group entry, so `op` needs human review if Windowsill treats the field strictly.

## Temperature values

Candidate values:

- `min_temp`: `15`
- `max_temp`: `33`
- `optimal_temp`: `26`
- `hardiness_temp`: `0`
- `hardiness_zone_min`: `10`

Rationale:

- Rutgers / US Basil Consortium gives a general basil optimal growth range of 21–32°C.
- Basil is warm-season and cold-sensitive.
- `min_temp: 15` is a practical lower active-growth threshold.
- `optimal_temp: 26` better fits a warm basil model than the existing `23`.
- `max_temp: 33` is a practical upper recommendation value before container heat and water stress become more likely.
- `hardiness_temp: 0` is used as a frost-boundary simplification, not an active-growth value.
- `hardiness_zone_min: 10` is retained as a broad warm-climate modelling value.

Uncertainty:

- These values are model estimates, not Purple-Basil-specific trial data.
- Colour intensity may depend on cultivar, light and growing conditions.

## Sun values

Candidate values:

- `sun_hours`: `6`
- `sun_direct`: `full`

Rationale:

- Rutgers supports at least six hours of direct sun for basil.
- UMN supports six to eight hours of bright light for basil.
- Strong light is especially relevant for purple-leaf colour quality.

Uncertainty:

- Indoor windowsill light is not the same as outdoor direct sun.
- Weak indoor light may reduce growth and colour quality.

## grow_time_weeks

Candidate value:

- `grow_time_weeks`: `7`

Locked meaning:

- Estimated weeks from seed/sowing to first realistic edible harvest.

Rationale:

- Existing `grow_time_weeks: 7` is plausible under warm, bright conditions.
- Purple cultivars can vary, so this should remain a cautious estimate.

## weeks_from_transplant

Candidate value:

- `weeks_from_transplant`: `4`

Locked meaning:

- Estimated weeks from transplanting or buying a young plant to first realistic edible harvest.

Rationale:

- Existing `weeks_from_transplant: 3` may be possible for very small picking, but `4` is a safer useful-harvest estimate.

## Context fit

Candidate context:

- `windowsill`
- `balcony`
- `garden`

### Windowsill

Good, with conditions. Needs warmth, drainage, airflow and strong light. Winter windowsills in northern regions may need supplemental light.

### Balcony

Good, seasonally. Works in containers if kept warm, sunny and watered. Cold wind and cold nights are problems.

### Garden

Good during frost-free season. Treat as annual in temperate climates. Avoid overcrowding and wet foliage.

## Safety and edible part

Candidate edible use:

- Normal culinary use of leaves and tender stems.

Rationale:

- Kew supports food use for `Ocimum basilicum` at species level.
- Iowa State supports basil leaves and stems as food-use parts.
- Iowa State notes purple basil is best enjoyed fresh, especially in salads and flavoured vinegars.

Boundary:

- This entry is only about normal culinary use.
- Other uses are outside the scope of this Windowsill edible-plant entry.
