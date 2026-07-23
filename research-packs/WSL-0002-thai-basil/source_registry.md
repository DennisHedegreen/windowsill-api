# Source registry — WSL-0002 Thai Basil

Status: audit draft  
Plant: Thai Basil  
Candidate ID: WSL-0002  
Folder: `research-packs/WSL-0002-thai-basil/`

## Repository sources

### 1. Windowsill production index

URL: https://github.com/DennisHedegreen/windowsill-api/blob/main/plants/index.json

Supports:

- Current production count is 148.
- `WSL-0002-thai-basil.json` is the second listed production plant file.
- This is an audit of an existing production entry, not a new live plant.

Does not support:

- Botanical correctness.
- Temperature values.
- Edibility or safety.
- Container or climate fit.

### 2. Existing production plant file — WSL-0002 Thai Basil

URL: https://github.com/DennisHedegreen/windowsill-api/blob/main/plants/WSL-0002-thai-basil.json

Supports:

- Existing entry ID: `WSL-0002`.
- Existing English name: `Thai Basil`.
- Existing Danish name: `Thai Basilikum`.
- Existing candidate Latin name: `Ocimum basilicum var. thyrsiflora`.
- Existing values being audited: temperature, sun, context, grow time, hardiness, habit and notes.

Does not support:

- That the values are verified.
- That the infraspecific name is taxonomically accepted.
- That `species: "basil"` is correct as a taxonomic species field.
- That `max_temp: 38` is appropriate for a Windowsill active-growth recommendation threshold.

## Botanical / taxonomic sources

### 3. Plants of the World Online — Kew Science, Ocimum basilicum L.

URL: https://powo.science.kew.org/taxon/urn:lsid:ipni.org:names:452874-1

Supports:

- `Ocimum basilicum L.` is an accepted species.
- The plant belongs to family `Lamiaceae` and genus `Ocimum`.
- Species-level native range and broad food-use status.
- The entry can be grounded at species level as `Ocimum basilicum`.
- Kew lists only two accepted infraspecifics for the species: `Ocimum basilicum var. basilicum` and `Ocimum basilicum var. minimum`.

Does not support:

- `Ocimum basilicum var. thyrsiflora` as an accepted infraspecific taxon.
- Thai Basil as a formally accepted botanical variety.
- Exact Windowsill model values.
- Exact container suitability or harvest timing.

### 4. Iowa State University Extension — Growing Basil in the Home Garden

URL: https://yardandgarden.extension.iastate.edu/how-to/growing-basil-home-garden

Supports:

- Basil is `Ocimum basilicum`, a member of the mint family.
- Basil is tender, cold-sensitive and readily damaged by frost.
- Basil can be grown indoors in a sunny window.
- Basil is well-suited for containers.
- Thai basil is described as a variety of sweet basil: `Ocimum basilicum var. thyrsiflora`.
- Thai basil cultivars are described as having narrow leaves, purple stems, pinkish-purple flowers and sweet/anise/licorice-like flavour.
- Popular Thai basil cultivars include `Thai`, `Sweet Thai` and `Siam Queen`.
- Basil leaves and stems are used fresh and dry in food contexts.

Does not support:

- Kew-level acceptance of the infraspecific name.
- Exact Windowsill `min_temp`, `max_temp`, `optimal_temp`, `grow_time_weeks` or `weeks_from_transplant`.
- Essential-oil or supplement safety.

### 5. University of Minnesota Extension — Growing basil in home gardens

URL: https://extension.umn.edu/vegetables/growing-basil

Supports:

- Common/sweet basil is `Ocimum basilicum` and belongs to `Lamiaceae`.
- Basil is a tender annual used for aromatic leaves.
- Basil needs at least 6–8 hours of bright light and well-drained soil.
- Thai basil is listed as `O.b.` and described as upright, well-branched, 24–36 inches, purple-stemmed/flowered and good for Asian cuisine.
- Seeds can germinate in about 5–7 days under suitable conditions.
- Containers dry out faster than garden beds.
- Indoor basil may need artificial light during darker periods.
- Flowering reduces productivity and can make flavour more bitter.

Does not support:

- The exact taxonomic rank of Thai basil.
- Exact Thai-basil-specific temperature thresholds.
- Exact Thai-basil-specific harvest timing under Windowsill’s locked meaning.

## Growing / climate sources

### 6. US Basil Consortium / Rutgers — Growing Basil in a Commercial Setting

URL: https://usbasilconsortium.rutgers.edu/grower-research-resources/grower-resources/growing-basil-in-a-commercial-setting/

Supports:

- Thai basil is listed as one of the popular basil types.
- Basil requires full sunlight and at least six hours of direct sunlight per day.
- Optimal basil growth temperature range is given as 70–90°F / 21–32°C.
- Basil should be grown in fertile, well-drained soil with good moisture retention.
- Harvest begins once plants reach sufficient size.

Does not support:

- Exact Thai-basil-specific heat limit.
- Windowsill winter performance.
- Exact first realistic edible harvest timing for Thai basil.
- The infraspecific taxonomy of Thai basil.

### 7. The Spruce — How to Grow Thai Basil in Your Herb Garden

URL: https://www.thespruce.com/thai-basil-7375163

Supports:

- Thai basil is commonly labelled `Ocimum basilicum var. thyrsiflora` in horticultural/gardening guidance.
- Thai basil has edible leaves and is used in Southeast Asian cuisines.
- It is generally hardy only in USDA zones 10–11 and grown as an annual in colder contexts.
- It grows best with at least six hours of direct sun per day.
- It prefers warm conditions; planting outside is recommended only when day and night temperatures are warm enough.
- Thai basil can grow in containers.
- Thai basil started from seed can be ready to harvest in as little as seven weeks, depending on cultivar and conditions.

Does not support:

- Formal botanical acceptance.
- Production-grade expert review.
- Universal timing under all climates, seasons, orientations or indoor light levels.
- Safety of essential oils, supplements, extracts or medicinal dosing.

## Safety sources

### 8. BfR — Alkenylbenzenes in food: How large is the health risk?

URL: https://www.bfr.bund.de/cm/349/alkenylbenzenes-in-food-how-large-is-the-health-risk.pdf

Supports:

- Certain herbs and spices, including basil, may naturally contain alkenylbenzenes.
- Basil-containing pesto and plant-based food supplements may contain high amounts of alkenylbenzenes.
- Estragole, methyleugenol and safrole have mutagenic/carcinogenic concern in animal studies.
- The risk picture has knowledge gaps and cannot be conclusively assessed for all alkenylbenzene-containing foods.

Does not support:

- That normal culinary use of Thai basil leaves is unsafe.
- A specific home-consumption dose limit.
- Any claim that Windowsill should recommend medicinal or supplement use.
- Thai-basil-specific alkenylbenzene content.

## Personal observation

No personal observation was provided for this WSL-0002 audit pack.

## Source quality notes

- Strong species-level botanical support: Kew POWO.
- Strong practical basil-growing support: Iowa State Extension, University of Minnesota Extension and Rutgers / US Basil Consortium.
- Thai-basil-specific identity support exists from Iowa State and The Spruce, but the infraspecific name remains uncertain because Kew POWO does not list `var. thyrsiflora` among accepted infraspecifics.
- Thai-basil-specific timing support is weaker than general basil-growing support.
- Safety boundary support is general basil/herb safety, not Thai-basil-specific.
