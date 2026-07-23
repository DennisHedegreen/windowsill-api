# Source registry — WSL-0003 Lemon Basil

Status: audit draft  
Plant: Lemon Basil  
Candidate ID: WSL-0003  
Folder: `research-packs/WSL-0003-lemon-basil/`

## Repository sources

### 1. Windowsill production index

URL: https://github.com/DennisHedegreen/windowsill-api/blob/main/plants/index.json

Supports:

- `WSL-0003-lemon-basil.json` is part of the current production library.
- This pack is an audit of an existing production entry, not a new live plant.

Does not support:

- Botanical correctness.
- Temperature values.
- Edibility or safety.
- Container or climate fit.

### 2. Existing production plant file — WSL-0003 Lemon Basil

URL: https://github.com/DennisHedegreen/windowsill-api/blob/main/plants/WSL-0003-lemon-basil.json

Supports:

- Existing entry ID: `WSL-0003`.
- Existing English name: `Lemon Basil`.
- Existing Danish name: `Citron Basilikum`.
- Existing candidate Latin name: `Ocimum × citriodorum`.
- Existing type: `hybrid`.
- Existing values being audited: temperature, sun, context, grow time, hardiness, habit and notes.

Does not support:

- That `Ocimum × citriodorum` is the currently preferred accepted botanical name.
- That `species: "basil"` is correct as a taxonomic species field.
- That `sun_hours: 5`, `optimal_temp: 22`, `grow_time_weeks: 6`, `weeks_from_transplant: 3` or `hardiness_temp: -1` are verified values.
- That the plant has been expert reviewed.

## Botanical / taxonomic sources

### 3. Plants of the World Online — Kew Science, Ocimum basilicum L.

URL: https://powo.science.kew.org/taxon/urn:lsid:ipni.org:names:452874-1

Supports:

- `Ocimum basilicum L.` is an accepted species.
- `Ocimum basilicum` belongs to family `Lamiaceae` and genus `Ocimum`.
- Species-level food-use context for basil.
- One parent identity used in lemon-basil hybrid explanations.

Does not support:

- `Ocimum × citriodorum` as the accepted name for Lemon Basil.
- `Ocimum × africanum` as the accepted name for Lemon Basil in this pack, because this specific source page is for `Ocimum basilicum`.
- Exact Windowsill model values.

### 4. Wikipedia — Lemon basil

URL: https://en.wikipedia.org/wiki/Lemon_basil

Supports:

- Lemon basil is commonly presented as `Ocimum × africanum`.
- The page lists `Ocimum citriodorum` as a synonym.
- The plant is described as a hybrid between `Ocimum basilicum` and `Ocimum americanum`.
- The plant is described as grown for lemon scent and used in cooking.
- It gives rough plant height and culinary-use context.
- It notes general basil-like care: tropical/warm, at least six hours direct sunlight, flowering reduces leaf quality.

Does not support:

- Production-grade taxonomic certainty by itself.
- Exact Windowsill temperature, harvest timing or context-fit values.
- Safety of extracts, essential oil, supplements, medicinal dosing or seed-gel use.

### 5. Wikipedia — Limonenbasilikum

URL: https://de.wikipedia.org/wiki/Limonenbasilikum

Supports:

- Lemon basil is described as `Ocimum × africanum`.
- It is described as a hybrid of `Ocimum americanum` and `Ocimum basilicum`.
- It is described as a spice/culinary plant with lemon aroma.
- It treats `Ocimum × citriodorum` as a synonym.
- It gives broad distribution/use context.

Does not support:

- Expert-reviewed Windowsill field values.
- Container performance.
- Indoor windowsill performance.
- Exact harvest timing.

### 6. Wikipedia — Basil

URL: https://en.wikipedia.org/wiki/Basil

Supports:

- Basil is a culinary herb in `Lamiaceae`.
- Basil is tender and cold-sensitive.
- Basil is used fresh in food and has many varieties/hybrids.
- The page notes lemon basil as a hybrid involving `Ocimum basilicum` and `Ocimum americanum`.

Does not support:

- Exact Lemon Basil taxonomy alone.
- Exact Windowsill model values.
- Essential-oil or supplement safety.

## Growing / climate sources

### 7. University of Minnesota Extension — Growing basil in home gardens

URL: https://extension.umn.edu/vegetables/growing-basil

Supports:

- Basil is a tender annual used for aromatic leaves.
- Basil needs at least 6–8 hours of bright light and well-drained soil.
- Seeds can germinate in about 5–7 days under suitable conditions.
- Containers dry out faster than garden beds.
- Indoor basil may need artificial light during darker periods.
- Flowering reduces productivity and can make flavour more bitter.

Does not support:

- Lemon Basil-specific accepted botanical naming.
- Exact Lemon Basil-specific temperature thresholds.
- Exact Lemon Basil-specific harvest timing under Windowsill’s locked meaning.

### 8. Iowa State University Extension — Growing Basil in the Home Garden

URL: https://yardandgarden.extension.iastate.edu/how-to/growing-basil-home-garden

Supports:

- Basil is `Ocimum basilicum`, a member of the mint family.
- Basil is tender, cold-sensitive and readily damaged by frost.
- Basil can be grown indoors in a sunny window.
- Basil is well-suited for containers.
- Basil leaves and stems are used fresh and dry in food contexts.

Does not support:

- Lemon Basil-specific botanical naming.
- Exact Windowsill `min_temp`, `max_temp`, `optimal_temp`, `grow_time_weeks` or `weeks_from_transplant`.
- Essential-oil or supplement safety.

### 9. US Basil Consortium / Rutgers — Growing Basil in a Commercial Setting

URL: https://usbasilconsortium.rutgers.edu/grower-research-resources/grower-resources/growing-basil-in-a-commercial-setting/

Supports:

- Basil requires full sunlight and at least six hours of direct sunlight per day.
- Optimal basil growth temperature range is given as 70–90°F / 21–32°C.
- Basil should be grown in fertile, well-drained soil with good moisture retention.
- Harvest begins once plants reach sufficient size.

Does not support:

- Exact Lemon Basil-specific heat limit.
- Windowsill winter performance.
- Exact first realistic edible harvest timing for Lemon Basil.
- Lemon Basil taxonomy.

### 10. The Spruce — 17 Types of Basil to Grow in Your Herb Garden

URL: https://www.thespruce.com/types-of-basil-6500081

Supports:

- Lemon Basil is treated as an edible basil type with citrus flavour and South/Southeast Asian culinary use.
- It uses `Ocimum basilicum citriodorum` as a label, showing naming inconsistency in horticultural sources.
- It gives practical gardening/culinary context.

Does not support:

- Accepted botanical name.
- Exact Windowsill model values.
- Safety beyond ordinary culinary use.

## Safety sources

### 11. BfR — Alkenylbenzenes in food: How large is the health risk?

URL: https://www.bfr.bund.de/cm/349/alkenylbenzenes-in-food-how-large-is-the-health-risk.pdf

Supports:

- Certain herbs and spices, including basil, may naturally contain alkenylbenzenes.
- Basil-containing pesto and plant-based food supplements may contain high amounts of alkenylbenzenes.
- Estragole, methyleugenol and safrole have mutagenic/carcinogenic concern in animal studies.
- The risk picture has knowledge gaps and cannot be conclusively assessed for all alkenylbenzene-containing foods.

Does not support:

- That normal culinary use of Lemon Basil leaves is unsafe.
- A specific home-consumption dose limit.
- Any claim that Windowsill should recommend medicinal, extract or supplement use.
- Lemon-Basil-specific alkenylbenzene content.

## Personal observation

No personal observation was provided for this WSL-0003 audit pack.

## Source quality notes

- Strong general basil-growing support: UMN Extension, Iowa State Extension, Rutgers / US Basil Consortium.
- Strong species-level support for `Ocimum basilicum`: Kew POWO.
- Lemon-Basil-specific naming support is weaker and partly secondary: Wikipedia pages and gardening sources disagree between `Ocimum × africanum`, `Ocimum × citriodorum`, and `Ocimum basilicum citriodorum`.
- Main required human check: preferred botanical name and how Windowsill should store hybrid names in `name_latin` and `species`.
- Safety boundary support is general basil/herb safety, not Lemon-Basil-specific.
