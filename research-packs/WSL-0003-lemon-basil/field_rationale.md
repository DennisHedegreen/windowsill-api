# Field rationale — WSL-0003 Lemon Basil

## Summary

This is an audit pack for the existing Windowsill plant entry `plants/WSL-0003-lemon-basil.json`.

The existing entry is plausible, but several fields need tightening:

- `name_latin: "Ocimum × citriodorum"` may be better treated as a synonym or horticultural label, with `Ocimum × africanum` as the candidate accepted name.
- `species: "basil"` should not be used if the field is taxonomic.
- `sun_hours: 5` is probably too low for a full-sun basil recommendation.
- `optimal_temp: 22` is probably too cool as the sweet spot for a warm-season basil.
- `grow_time_weeks: 6` and `weeks_from_transplant: 3` are optimistic for a useful culinary harvest.
- `hardiness_temp: -1` risks implying frost tolerance; basil should be treated as frost-sensitive.

## Botanical identity

Candidate value:

- `name_latin`: `Ocimum × africanum`

Rationale:

- The existing production entry uses `Ocimum × citriodorum`.
- Lemon-basil-specific secondary sources commonly describe lemon basil as a hybrid between `Ocimum basilicum` and `Ocimum americanum`.
- Several sources treat `Ocimum × africanum` as the accepted or preferred name and `Ocimum × citriodorum` as a synonym.
- The plant is kept as `type: "hybrid"`, which matches the hybrid-origin interpretation.

Uncertainty:

- This pack did not obtain a directly parsed Kew POWO page for `Ocimum × africanum`.
- Lemon basil naming is messy in horticultural sources: `Ocimum × africanum`, `Ocimum × citriodorum`, `Ocimum basilicum citriodorum` and cultivar-specific lemon basils are all seen.
- `Mrs. Burns' Lemon` basil is not the same thing as this Lemon Basil candidate and should not be silently mixed into this entry.
- Expert review should decide whether Windowsill should store `name_latin` as `Ocimum × africanum`, keep `Ocimum × citriodorum`, or use a broader note-based label.

## Family / genus / species

Candidate values:

- `family`: `Lamiaceae`
- `genus`: `Ocimum`
- `species`: `africanum`

Rationale:

- The candidate botanical name is `Ocimum × africanum`.
- `africanum` is the epithet part of the hybrid name.
- `type: "hybrid"` carries the hybrid status because the current schema has no separate hybrid-marker field.
- `species: "basil"` in the existing production file reads like a common-name fragment, not a taxonomic epithet.

Uncertainty:

- If Windowsill later adds a proper hybrid-name convention, this field may need revision.
- The current pack does not add new schema fields, so the hybrid marker is preserved only through `name_latin` and `type`.

## Type

Candidate value:

- `type`: `hybrid`

Rationale:

- The existing production entry already uses `hybrid`.
- Lemon basil is commonly described as a hybrid between `Ocimum basilicum` and `Ocimum americanum`.

Uncertainty:

- Seed lots sold as "lemon basil" may include different cultivar lines, synonyms or lemon-scented sweet basil cultivars.
- The broad Windowsill entry should not claim every marketed lemon basil is genetically identical.

## Temperature values

Candidate values:

- `min_temp`: `15`
- `max_temp`: `33`
- `optimal_temp`: `26`
- `hardiness_temp`: `0`
- `hardiness_zone_min`: `10`

Rationale:

- General basil sources support basil as warm-season, tender and cold-sensitive.
- Rutgers / US Basil Consortium gives a general basil optimal growth range of 21–32°C.
- `min_temp: 15` is a practical lower active-growth threshold, not a survival threshold.
- Existing `optimal_temp: 22` is inside the Rutgers range but too close to the cool edge for a warm-season basil model.
- `optimal_temp: 26` better represents the warm basil sweet spot while staying inside the cited 21–32°C range.
- `max_temp: 33` is kept close to the existing `33` because the Rutgers optimum upper end is 32°C, and container heat/water stress becomes increasingly likely above that.
- `hardiness_temp: 0` is used as a frost-boundary / kill-risk simplification, not as a claim that the plant grows at 0°C.
- `hardiness_zone_min: 10` is retained because basil is perennial only in warm/no-frost contexts and annual elsewhere.

Uncertainty:

- The source data separates germination, active growth, survival, cold damage, heat tolerance and greenhouse conditions.
- Windowsill compresses these into a few fields, so all numeric values are model estimates.
- Lemon basil may vary by seed strain/cultivar.

## Sun values

Candidate values:

- `sun_hours`: `6`
- `sun_direct`: `full`

Rationale:

- Rutgers says basil needs at least six hours of direct sunlight per day.
- UMN says basil needs at least six to eight hours of bright light.
- Lemon-basil-specific secondary sources also describe it as needing at least six hours of direct sunlight.
- Existing `sun_hours: 5` is probably too low for a robust full-sun basil recommendation.

Uncertainty:

- Indoor windowsill light is not equivalent to outdoor direct sun.
- A north-facing winter windowsill should not be treated as a good Lemon Basil recommendation without grow light support.
- In very hot balcony/garden situations, afternoon shade may still be useful even though the model says `sun_direct: "full"`.

## grow_time_weeks

Candidate value:

- `grow_time_weeks`: `7`

Locked meaning:

- Estimated weeks from seed/sowing to first realistic edible harvest.

Rationale:

- Existing `grow_time_weeks: 6` may be possible for small early pinching under strong conditions.
- A first useful culinary harvest is more realistically modelled around 7 weeks under warm, bright conditions.
- General basil harvest sources often point to roughly 60–70 days for substantial harvest, but first edible leaf use can happen earlier.
- The value should represent first realistic edible harvest, not full maturity or maximum repeated harvest.

Uncertainty:

- Lemon basil can vary by cultivar/seed line.
- Cooler windowsills, low light, overcrowding and poor drainage can delay harvest.
- If Windowsill wants a conservative repeated-harvest value, 8 weeks may be safer.

## weeks_from_transplant

Candidate value:

- `weeks_from_transplant`: `4`

Locked meaning:

- Estimated weeks from transplanting or buying a young plant to first realistic edible harvest.

Rationale:

- Existing `weeks_from_transplant: 3` is optimistic but not impossible for small early picking.
- A 4-week estimate is safer for a young plant to settle, branch and produce a useful harvest.
- Basil responds to pinching and regrowth, but the plant should not be stripped too early.

Uncertainty:

- No strong source in this pack directly gives Lemon-Basil-specific weeks from transplant under the Windowsill definition.
- This is a model estimate and needs human check.

## Context fit

Candidate context:

- `windowsill`
- `balcony`
- `garden`

### Windowsill: good, with conditions

Supported because:

- Basil can be grown indoors in a sunny window.
- Lemon basil is a compact herb and can fit containers.
- Windowsill growing is realistic if light, warmth, drainage and airflow are adequate.

Caution:

- Indoor winter light can be insufficient in northern regions.
- Cold glass and drafts can stunt growth.
- A grow light may be needed for reliable winter production.

### Balcony: good, seasonal

Supported because:

- Basil works well in containers.
- Lemon basil remains small enough for balcony pots.
- Warm balconies can provide the sun and heat basil needs.

Caution:

- Small pots dry quickly.
- Cold wind and cold nights can damage plants.
- Very hot balconies can require more water or afternoon shade.

### Garden: good, frost-free season

Supported because:

- Basil is a standard warm-season garden herb.
- Lemon basil can be grown outdoors after frost risk.
- Regular pinching supports leaf production.

Caution:

- Not suitable for frost season.
- Wet, crowded planting can raise disease pressure.
- Treat as annual in temperate climates.

## Safety and edible part

Candidate edible use:

- Normal culinary use of leaves and tender stems.

Rationale:

- Lemon basil is widely described as a culinary herb.
- General basil sources support culinary use of basil leaves and stems.
- Lemon-basil-specific sources describe use in Southeast Asian and other cuisines.

Safety boundary:

- This entry covers normal culinary leaf/tender-stem use.
- It does not cover essential oil, extracts, supplements, medicinal dosing, high-dose use, pregnancy-specific safety, allergy risk or seed-gel use.
- BfR flags alkenylbenzenes in herbs such as basil and higher-exposure contexts such as pesto, extracts and plant-based supplements.
- Do not promote Lemon Basil as medicinal.
