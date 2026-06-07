# Field rationale — WSL-0001 Genovese Basil

## Summary

This is an audit pack for the existing Windowsill plant entry `WSL-0001-genovese-basil.json`.

The existing entry is broadly plausible, but several fields needed tightening:

- `species` should be `basilicum`, not `basil`, if the field is taxonomic.
- `max_temp: 35` is probably too optimistic as an active-growth comfort value.
- `grow_time_weeks: 6` and `weeks_from_transplant: 3` are optimistic for a useful culinary harvest.
- `hardiness_temp: -1` risks suggesting frost tolerance; basil should be treated as frost-sensitive.

## Botanical name

Candidate value:

```json
"name_latin": "Ocimum basilicum 'Genovese'"
```

Rationale:

- Kew POWO supports `Ocimum basilicum L.` as an accepted species.
- Genovese is treated here as a cultivar/type label within `Ocimum basilicum`.
- De Bolster and Johnny's list Genovese basil as `Ocimum basilicum` seed.

Uncertainty:

- "Genovese" in seed trade can mean a cultivar, cultivar group, type, or regional/DOP-associated production name depending on source.
- This pack should not claim that every "Genovese Basil" product is genetically identical.

## Family / genus / species

Candidate values:

```json
"family": "Lamiaceae",
"genus": "Ocimum",
"species": "basilicum"
```

Rationale:

- Kew's windowsill basil leaflet identifies basil as `Ocimum` and a member of Lamiaceae.
- POWO supports `Ocimum basilicum L.` as accepted.
- Existing `species: "basil"` reads like a common-name fragment rather than a taxonomic species epithet.

## Type

Candidate value:

```json
"type": "op"
```

Rationale:

- De Bolster lists its Genovese basil as `zaadvast ras`, meaning a fixed/open seed variety rather than an F1 hybrid.
- The broad Windowsill entry is not tied to one seed company, so this is kept as plausible but not absolute.

Uncertainty:

- Some Genovese-type cultivars may be proprietary, compact, disease-resistant or F1 lines. The field should be human-checked if Windowsill wants strict cultivar genetics.

## Temperature model

Candidate values:

```json
"min_temp": 15,
"max_temp": 32,
"optimal_temp": 26,
"hardiness_temp": 0,
"hardiness_zone_min": 10
```

Rationale:

- Rutgers / US Basil Consortium gives an optimal basil growth range of 21–32°C.
- Iowa State Extension says basil is cold-sensitive, frost-damaged, and should be direct-sown outdoors only after night temperatures are consistently above about 50°F / 10°C.
- `min_temp: 15` is used as an active-growth threshold, not as survival. Basil may survive cooler nights briefly, but performance drops and frost risk matters.
- `max_temp: 32` replaces the existing `35` because 21–32°C is better supported as the optimum/comfort range.
- `optimal_temp: 26` is a central modelling value inside the 21–32°C range.
- `hardiness_temp: 0` is used only as a frost boundary / death-risk simplification, not as a claim that the plant is happy at 0°C.
- `hardiness_zone_min: 10` is kept because basil behaves as a tender perennial only in very warm/no-frost contexts and as an annual in temperate climates.

Uncertainty:

- The source data separates germination, active growth, transplant safety, frost damage and commercial greenhouse conditions. Windowsill compresses those into a few fields, so these values are model estimates.

## Sun model

Candidate values:

```json
"sun_hours": 6,
"sun_direct": "full"
```

Rationale:

- Rutgers / US Basil Consortium says basil requires at least six hours of direct sunlight per day.
- University of Minnesota Extension says basil requires six to eight hours of bright light.
- Kew says basil loves a sunny windowsill.

Uncertainty:

- Bright outdoor sun, balcony sun and indoor windowsill light are not equivalent. A north-facing winter windowsill should not be treated as equivalent to six hours of direct summer sun.

## Context fit

Candidate context:

```json
"context": ["windowsill", "balcony", "garden"]
```

### Windowsill: good, with conditions

Supported because:

- Kew explicitly describes windowsill basil growing and recommends a sunny windowsill.
- Iowa State Extension says basil can be grown indoors in a sunny window.

Caution:

- Indoor basil may have less intense flavour/fragrance and may need artificial light in darker periods.
- Supermarket basil pots can fail because of crowding, weak light, poor airflow and overwatering; this is a practical warning, not a reason to exclude the windowsill context.

### Balcony: good, with warmth

Supported because:

- Basil performs well in containers.
- A sunny balcony can provide full sun and air circulation.
- De Bolster's 20 × 20 cm spacing and 20–50 cm height make balcony containers realistic.

Caution:

- Cold, wind and night temperatures below safe outdoor thresholds can damage plants.

### Garden: good, seasonal

Supported because:

- University extension sources describe basil as a standard home-garden herb.
- It should be planted after frost danger and in full sun with well-drained soil.

Caution:

- Not suitable for frost season.
- Disease pressure, especially downy mildew, may matter in wet/crowded conditions.

## Growth time

Candidate values:

```json
"grow_time_weeks": 8,
"weeks_from_transplant": 5
```

Rationale:

- Johnny's lists Genovese basil at 68 days to maturity from seeding date, which is close to 10 weeks.
- PanAmerican's compact Everleaf Genovese cultivar lists 30–45 days from transplant, roughly 4–6 weeks, but this is cultivar-specific.
- Kew notes that small basil leaves can be picked as micro-herbs earlier, but that is not the same as a useful full culinary plant.

Why not keep the existing values?

- Existing `grow_time_weeks: 6` may be possible for first picking under strong conditions, but it is optimistic for a normal user expecting a useful basil plant.
- Existing `weeks_from_transplant: 3` is likely too optimistic except for very small early picking.

Uncertainty:

- If Windowsill models "first edible leaves" instead of "useful harvest," `grow_time_weeks` could be lower. If it models full seed-to-maturity, it could be 9–10.

## Edibility and safety

Candidate note:

```json
"notes": "Use leaves for normal culinary purposes; flowers are also edible according to Kew guidance. Do not treat essential oil, medicinal dosing or high-concentrate extracts as covered by this edible-plant entry."
```

Rationale:

- Kew supports leaves as raw/cooked culinary food and flowers as edible.
- Basil is a common culinary herb.
- BfR flags naturally occurring alkenylbenzenes in herbs such as basil and notes higher concern contexts such as basil-containing pesto, extracts and supplements.
- Wageningen/Food and Chemical Toxicology summary concerns natural flavour complexes under intended flavour use and explicitly does not cover supplements.

Safety boundary:

- Windowsill should recommend the plant for normal culinary leaf/flower use.
- Windowsill should not imply safety for essential oils, concentrated extracts, medicinal dosing or supplement use.
