# Field rationale — WSL-0002 Thai Basil

## Summary

This is an audit pack for the existing Windowsill plant entry `plants/WSL-0002-thai-basil.json`.

The existing entry is broadly plausible, but several fields need tightening:

- `species` should be `basilicum`, not `basil`, if the field is taxonomic.
- `name_latin: "Ocimum basilicum var. thyrsiflora"` is useful as a horticultural label, but it needs botanical review because Kew POWO supports `Ocimum basilicum L.` at species level and does not list `var. thyrsiflora` among accepted infraspecifics.
- `max_temp: 38` is probably too optimistic as an active-growth quality threshold.
- `hardiness_temp: -1` risks implying frost tolerance; basil should be treated as frost-sensitive.
- `type: "op"` is carried forward provisionally but not directly source-confirmed in this pack.

## Botanical identity

Candidate value:

- `name_latin`: `Ocimum basilicum var. thyrsiflora`

Rationale:

- The existing production entry uses `Ocimum basilicum var. thyrsiflora`.
- Iowa State Extension describes Thai basil as a variety of sweet basil and gives the same infraspecific name.
- The Spruce also uses the same botanical label for Thai basil.
- Kew POWO supports `Ocimum basilicum L.` as an accepted species, which is the safest species-level grounding.

Uncertainty:

- Kew POWO does not list `var. thyrsiflora` among accepted infraspecifics for `Ocimum basilicum`.
- Some sources use spelling variants such as `thyrsiflora` and `thyrsiflorum`.
- Thai basil, holy basil and lemon basil are often confused in culinary contexts.
- This pack should not claim final botanical certainty until expert review confirms the preferred Windowsill naming convention.

## Family / genus / species

Candidate values:

- `family`: `Lamiaceae`
- `genus`: `Ocimum`
- `species`: `basilicum`

Rationale:

- Kew POWO supports `Ocimum basilicum L.` as an accepted species in `Lamiaceae`.
- Iowa State and UMN both treat culinary basil as `Ocimum basilicum`.
- The existing `species: "basil"` reads like a common-name fragment, not a taxonomic species epithet.

## Type

Candidate value:

- `type`: `op`

Rationale:

- The existing production entry uses `op`.
- Many Thai basil seed lines are sold as ordinary seed cultivars rather than explicitly as F1 hybrids.

Uncertainty:

- This pack did not find a strong source confirming that the broad Windowsill Thai Basil entry should always be treated as open-pollinated.
- Keep `type: "op"` only as a provisional carry-forward value unless Windowsill has a stricter cultivar/genetics policy.

## Temperature values

Candidate values:

- `min_temp`: `18`
- `max_temp`: `34`
- `optimal_temp`: `27`
- `hardiness_temp`: `0`
- `hardiness_zone_min`: `10`

Rationale:

- Rutgers / US Basil Consortium gives a general basil optimal growth range of 21–32°C.
- Thai basil is a warm-season basil type; a practical lower active-growth threshold of 18°C is more realistic than recommending it in cool conditions.
- `optimal_temp: 27` sits inside the cited basil optimum range and matches the warm-growth profile.
- `max_temp: 34` is a modelling threshold above the cited optimum range where heat stress, water stress or quality issues become more likely, especially in containers.
- Existing `max_temp: 38` may reflect survival or heat tolerance, but it is too aggressive for a recommendation threshold under the locked meaning of `max_temp`.
- Iowa State supports cold sensitivity and frost damage.
- `hardiness_temp: 0` is used as a frost boundary / survival-risk simplification, not as an active-growth temperature.
- `hardiness_zone_min: 10` is consistent with Thai basil being treated as perennial only in warm/no-frost contexts and annual elsewhere.

Uncertainty:

- The values compress several different biological thresholds into a small model: germination, active growth, transplant safety, survival, cold damage and heat stress.
- Thai basil may tolerate hotter conditions than Genovese basil if watered and partially shaded, but `max_temp` is about recommendation quality, not absolute survival.

## Sun values

Candidate values:

- `sun_hours`: `6`
- `sun_direct`: `full`

Rationale:

- Rutgers says basil requires at least six hours of direct sun per day.
- UMN says basil needs at least six to eight hours of bright light per day.
- The Spruce says Thai basil grows best with at least six hours of direct sun per day.
- The value is kept at `6` because it is the minimum realistic threshold for a recommendation.

Uncertainty:

- Outdoor six-hour sun, balcony sun and indoor windowsill light are not equivalent.
- A north-facing winter windowsill should not be treated as equivalent to six hours of direct summer sun.
- Very hot climates may require afternoon shade even though the model says `sun_direct: "full"`.

## grow_time_weeks

Candidate value:

- `grow_time_weeks`: `7`

Locked meaning:

- Estimated weeks from seed/sowing to first realistic edible harvest.

Rationale:

- The existing production entry uses `7`.
- The Spruce says Thai basil started from seed can be ready to harvest in as little as seven weeks depending on cultivar and conditions.
- UMN supports fast basil germination under suitable conditions, but germination is not the same as harvest.
- A seven-week estimate is plausible for first realistic edible leaf harvest under warm, bright conditions.

Uncertainty:

- This is not a universal maturity claim.
- Cooler windowsills, weak light, overcrowded supermarket-style pots or poor drainage can delay harvest.
- If Windowsill wants a conservative “useful repeated harvest” threshold instead of “first realistic edible harvest”, this may need to become 8 weeks.

## weeks_from_transplant

Candidate value:

- `weeks_from_transplant`: `4`

Locked meaning:

- Estimated weeks from transplanting or buying a young plant to first realistic edible harvest.

Rationale:

- The existing production entry uses `4`.
- If a user buys a young Thai basil plant or transplants a healthy seedling, edible top growth can realistically be harvested sooner than seed-grown plants.
- Iowa State supports ongoing harvest after plants are large enough and regrowth after cutting.

Uncertainty:

- No strong source in this pack directly gives Thai-basil-specific weeks from transplant to first Windowsill-style edible harvest.
- The value is a model estimate and should be human-checked.

## Context fit

Candidate context:

- `windowsill`
- `balcony`
- `garden`

### Windowsill: good, with conditions

Supported because:

- Iowa State says basil can be grown indoors in a sunny window.
- UMN says indoor basil may need artificial light during darker periods.
- Thai basil can work in a pot if warmth, light, drainage and airflow are adequate.

Caution:

- Dark winter windowsills are weak contexts.
- Cold glass, cold drafts and low light can stunt the plant.
- Windowsill success depends heavily on orientation and season.

### Balcony: good, seasonal

Supported because:

- Basil is well suited to containers.
- Thai basil fits container growing if the pot drains well and the plant gets enough sun.
- Balcony air circulation can be better than indoor windowsill air.

Caution:

- Cold wind and cold nights can damage the plant.
- Small pots dry fast.
- Very hot balconies can exceed the active-growth comfort range and require more water or afternoon shade.

### Garden: good, frost-free season

Supported because:

- Extension sources describe basil as a standard garden herb.
- Thai basil is a basil type grown for culinary and ornamental use.
- Garden planting should happen after frost danger and cold-night risk.

Caution:

- Not suitable for frost season.
- Overcrowding, wet foliage and poor airflow increase disease risk.
- It should be treated as annual in temperate climates.

## Safety and edible part

Candidate edible use:

- Normal culinary use of leaves and tender stems.

Rationale:

- Kew POWO supports broad food use of `Ocimum basilicum`.
- Iowa State says basil leaves and stems are used fresh and dry.
- UMN describes basil as a culinary herb used for aromatic leaves.
- Thai basil is specifically described as used in Asian / Southeast Asian cuisine.

Safety boundary:

- This entry covers normal culinary leaf/tender-stem use.
- It does not cover essential oil, extracts, supplements, medicinal dosing, high-dose use, pregnancy-specific safety or allergy risk.
- BfR flags alkenylbenzenes in herbs such as basil and higher-exposure contexts such as pesto, extracts and plant-based supplements.
- Do not casually promote Thai basil as medicinal.
