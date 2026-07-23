# Source registry — WSL-0004 Purple Basil

Status: audit draft  
Plant: Purple Basil  
Candidate ID: WSL-0004  
Folder: `research-packs/WSL-0004-purple-basil/`

## Repository sources

### 1. Windowsill production index

URL: https://github.com/DennisHedegreen/windowsill-api/blob/main/plants/index.json

Supports:

- `WSL-0004-purple-basil.json` is the fourth listed production plant file.
- Current production count is 148.
- This pack is an audit of an existing production entry, not a new live plant.

Does not support:

- Botanical correctness.
- Temperature values.
- Edibility or safety.
- Container or climate fit.

### 2. Existing production plant file — WSL-0004 Purple Basil

URL: https://github.com/DennisHedegreen/windowsill-api/blob/main/plants/WSL-0004-purple-basil.json

Supports:

- Existing entry ID: `WSL-0004`.
- Existing English name: `Purple Basil`.
- Existing Danish name: `Lilla Basilikum`.
- Existing candidate Latin name: `Ocimum basilicum 'Purpurascens'`.
- Existing values being audited: temperature, sun, context, grow time, hardiness, habit and notes.

Does not support:

- That `Ocimum basilicum 'Purpurascens'` is the correct botanical identity for all purple basil.
- That `species: "basil"` is correct as a taxonomic species field.
- That `optimal_temp: 23`, `weeks_from_transplant: 3` or `hardiness_temp: -1` are verified values.
- That the plant has been expert reviewed.

## Botanical / taxonomic sources

### 3. Plants of the World Online — Kew Science, Ocimum basilicum L.

URL: https://powo.science.kew.org/taxon/urn:lsid:ipni.org:names:452874-1

Supports:

- `Ocimum basilicum L.` is an accepted species.
- The species belongs to family `Lamiaceae` and genus `Ocimum`.
- The species has broad food-use status.
- Species-level grounding for purple-leaf sweet basil cultivars.
- Kew lists only two accepted infraspecifics for `Ocimum basilicum`: `var. basilicum` and `var. minimum`.

Does not support:

- `Ocimum basilicum 'Purpurascens'` as a universally accepted cultivar name.
- Purple Basil as one single cultivar.
- Exact Windowsill model temperatures, context fit or harvest timing.

### 4. Iowa State University Extension — Growing Basil in the Home Garden

URL: https://yardandgarden.extension.iastate.edu/how-to/growing-basil-home-garden

Supports:

- Basil is `Ocimum basilicum`, a member of the mint family.
- Basil is tender, cold-sensitive and readily damaged by frost.
- Basil can be grown indoors in a sunny window.
- Basil is well-suited for containers.
- Basil leaves and stems are used fresh and dry in food contexts.
- Several cultivars have burgundy or purple leaves.
- Purple-leaf basils are grown for ornamental foliage as well as culinary use.
- Popular purple-leaf cultivars include `Dark Opal`, `Purple Ruffles`, `Red Rubin`, `Amethyst` and `Aromatto`.
- Purple basil is best enjoyed fresh, particularly in salads and flavoured vinegars.
- Purple and green basil stems can be visually appealing in floral arrangements.

Does not support:

- Treating all purple basils as one cultivar.
- Exact Windowsill `min_temp`, `max_temp`, `optimal_temp`, `grow_time_weeks` or `weeks_from_transplant`.
- Essential-oil or supplement safety.

### 5. University of Minnesota Extension — Growing basil in home gardens

URL: https://extension.umn.edu/vegetables/growing-basil

Supports:

- Basil is a tender annual used for aromatic leaves.
- Basil needs at least 6–8 hours of bright light and well-drained soil.
- Seeds can germinate in about 5–7 days under suitable conditions.
- Containers dry out faster than garden beds.
- Indoor basil may need artificial light during darker periods.
- `Purple Ruffles` is mentioned as a slower-germinating basil variety that benefits from indoor sowing six to eight weeks before planting outside.
- Flowering reduces productivity and can make flavour more bitter.
- Purple-leafed varieties can have ornamental flowers.

Does not support:

- `Ocimum basilicum 'Purpurascens'` as the preferred name.
- Exact purple-basil-specific temperature thresholds.
- Exact purple-basil-specific harvest timing under Windowsill’s locked meaning.

## Growing / climate sources

### 6. US Basil Consortium / Rutgers — Growing Basil in a Commercial Setting

URL: https://usbasilconsortium.rutgers.edu/grower-research-resources/grower-resources/growing-basil-in-a-commercial-setting/

Supports:

- Basil requires full sunlight and at least six hours of direct sunlight per day.
- Optimal basil growth temperature range is given as 70–90°F / 21–32°C.
- Basil should be grown in fertile, well-drained soil with good moisture retention.
- Harvest begins once plants reach sufficient size.

Does not support:

- Exact Purple-Basil-specific heat limit.
- Windowsill winter performance.
- Exact first realistic edible harvest timing for Purple Basil.
- Purple Basil taxonomy.

### 7. The Spruce — 17 Types of Basil to Grow in Your Herb Garden

URL: https://www.thespruce.com/types-of-basil-6500081

Supports:

- Purple basil entries such as `Dark Opal` and `Osmin Purple` are treated as basil types/cultivars.
- `Dark Opal` is labelled `Ocimum basilicum 'Dark Opal'`.
- Purple/dark basil types are presented as culinary and ornamental.
- Purple basil is visually useful and can be used fresh as garnish/salad herb.

Does not support:

- Accepted botanical name for a generic Purple Basil entry.
- Exact Windowsill model values.
- Safety beyond ordinary culinary use.

### 8. Wikipedia — Basil / List of basil cultivars / Dark opal basil

URLs:

- https://en.wikipedia.org/wiki/Basil
- https://en.wikipedia.org/wiki/List_of_basil_cultivars
- https://en.wikipedia.org/wiki/Dark_opal_basil

Supports:

- Basil cultivar naming is complex and many basils are cultivars of `Ocimum basilicum`.
- Purple basil labels vary, including `Purple Delight`, `Purpurascens`, `Dark Opal`, `Red Rubin`, `Purple Ruffles` and `Osmin Purple`.
- `Dark Opal` is commonly treated as a cultivar of `Ocimum basilicum`.
- Purple colour is associated with anthocyanins in purple basil cultivars.

Does not support:

- Production-grade taxonomic certainty by itself.
- Exact Windowsill field values.
- Expert review.
- Safety of essential oils, extracts, supplements or medicinal dosing.

## Safety sources

### 9. BfR — Alkenylbenzenes in food: How large is the health risk?

URL: https://www.bfr.bund.de/cm/349/alkenylbenzenes-in-food-how-large-is-the-health-risk.pdf

Supports:

- Certain herbs and spices, including basil, may naturally contain alkenylbenzenes.
- Basil-containing pesto and plant-based food supplements may contain high amounts of alkenylbenzenes.
- Estragole, methyleugenol and safrole have mutagenic/carcinogenic concern in animal studies.
- The risk picture has knowledge gaps and cannot be conclusively assessed for all alkenylbenzene-containing foods.

Does not support:

- That normal culinary use of Purple Basil leaves is unsafe.
- A specific home-consumption dose limit.
- Any claim that Windowsill should recommend medicinal, extract or supplement use.
- Purple-Basil-specific alkenylbenzene content.

## Personal observation

No personal observation was provided for this WSL-0004 audit pack.

## Source quality notes

- Strong species-level botanical support: Kew POWO.
- Strong practical basil-growing support: Iowa State Extension, University of Minnesota Extension and Rutgers / US Basil Consortium.
- Strong purple-leaf practical support: Iowa State Extension.
- Purple-Basil-specific taxonomy remains uncertain because the generic entry likely represents a cultivar/type group, not one cultivar.
- Safety boundary support is general basil/herb safety, not Purple-Basil-specific.
