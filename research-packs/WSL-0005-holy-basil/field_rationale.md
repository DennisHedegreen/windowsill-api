# Field rationale — WSL-0005 Holy Basil

## Summary

This is an audit pack for the existing Windowsill plant entry `plants/WSL-0005-holy-basil.json`.

The existing entry is plausible, but several fields need review:

- `name_latin: "Ocimum tenuiflorum"` is retained as candidate identity, but source/trade confusion with other `Ocimum` species should be reviewed.
- `species: "basil"` should be `tenuiflorum` if the field is taxonomic.
- `max_temp: 40` is too high for a practical recommendation threshold.
- `hardiness_temp: -1` risks implying more cold tolerance than a warm-season basil relative normally has.
- The notes should avoid implying that Windowsill recommends medicinal use.

## Botanical identity

Candidate value:

- `name_latin`: `Ocimum tenuiflorum`

Rationale:

- The existing production entry already uses `Ocimum tenuiflorum`.
- Holy Basil / Tulsi is commonly identified as `Ocimum tenuiflorum`.
- It is distinct from sweet basil and Thai basil.

Uncertainty:

- Some horticultural sources use holy basil loosely and may include other `Ocimum` species.
- Some sources use older or synonym names such as `Ocimum sanctum`.
- Human/expert review should confirm the preferred Windowsill name and synonym handling.

## Family / genus / species

Candidate values:

- `family`: `Lamiaceae`
- `genus`: `Ocimum`
- `species`: `tenuiflorum`

Rationale:

- Holy Basil is placed in `Ocimum` and `Lamiaceae`.
- `tenuiflorum` is the species epithet in the candidate Latin name.
- Existing `species: "basil"` reads like a common-name fragment rather than a taxonomic epithet.

## Type

Candidate value:

- `type`: `op`

Rationale:

- The existing production entry uses `op`.
- Holy Basil is commonly seed-grown.

Uncertainty:

- This pack did not verify all commercial Holy Basil/Tulsi seed lines.
- Keep `op` as provisional unless Windowsill treats type as strict seed-line genetics.

## Temperature values

Candidate values:

- `min_temp`: `18`
- `max_temp`: `34`
- `optimal_temp`: `28`
- `hardiness_temp`: `0`
- `hardiness_zone_min`: `10`

Rationale:

- Holy Basil is a warm-climate basil relative and underperforms in cool conditions.
- `min_temp: 18` is retained as a practical active-growth threshold.
- `optimal_temp: 28` is retained because it fits the warmth-demanding profile and sits near the warm side of general basil guidance.
- Existing `max_temp: 40` may reflect heat survival or rough climate tolerance, but it is too high for a practical quality recommendation threshold.
- `max_temp: 34` is a more cautious upper recommendation value for container/home-growing conditions.
- `hardiness_temp: 0` is used as a frost-boundary simplification, not as an active-growth value.
- `hardiness_zone_min: 10` is retained as a broad warm-climate modelling value.

Uncertainty:

- The numeric values are model estimates.
- Holy Basil-specific controlled temperature data was not established in this pack.
- Container heat, water stress and wind exposure can change real-world outcomes.

## Sun values

Candidate values:

- `sun_hours`: `6`
- `sun_direct`: `full`

Rationale:

- General basil sources support at least six hours of direct sun or bright light.
- Holy-Basil-specific guidance also emphasizes plenty of sunlight.
- Existing `sun_hours: 6` and `sun_direct: "full"` are retained.

Uncertainty:

- Indoor windowsill light is not equivalent to outdoor direct sun.
- Northern winter windowsills may not provide enough light without supplemental support.

## grow_time_weeks

Candidate value:

- `grow_time_weeks`: `8`

Locked meaning:

- Estimated weeks from seed/sowing to first realistic edible harvest.

Rationale:

- Existing `grow_time_weeks: 8` is plausible and appropriately cautious for a warmth-demanding basil relative.
- First tiny leaves can appear earlier, but this field is about first realistic edible harvest.

Uncertainty:

- Holy Basil timing depends strongly on light, warmth, cultivar/seed line and pot conditions.
- If grown cold or under weak light, harvest can be delayed.

## weeks_from_transplant

Candidate value:

- `weeks_from_transplant`: `4`

Locked meaning:

- Estimated weeks from transplanting or buying a young plant to first realistic edible harvest.

Rationale:

- Existing `weeks_from_transplant: 4` is plausible.
- A transplanted young plant still needs time to settle and branch before useful harvesting.

Uncertainty:

- No strong source in this pack directly gives Holy-Basil-specific weeks from transplant under the Windowsill definition.
- This remains a model estimate.

## Context fit

Candidate context:

- `windowsill`
- `balcony`
- `garden`

### Windowsill

Acceptable, with conditions. Needs strong light, warmth, airflow and drainage. Cool northern windowsills are weak contexts, especially in winter.

### Balcony

Good, seasonally. Works in containers if kept warm, sunny and watered. Cold wind and cold nights are problems.

### Garden

Good during frost-free warm season. Treat as annual in temperate climates. Avoid cold periods and wet, crowded conditions.

## Safety and edible part

Candidate edible use:

- Normal culinary leaf use and tea-style leaf use.

Rationale:

- Holy Basil/Tulsi is used in culinary and tea contexts in several traditions.
- The plant is also widely discussed in traditional medicine, but that is outside Windowsill’s edible-plant recommendation scope.

Boundary:

- This entry is only about growing and normal food/tea use.
- Supplements, extracts, essential oil, medicinal dosing and health claims are outside the scope of this pack.
- Do not promote Holy Basil as a treatment for any condition in Windowsill production copy.
