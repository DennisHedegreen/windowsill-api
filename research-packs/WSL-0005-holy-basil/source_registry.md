# Source registry — WSL-0005 Holy Basil

Status: audit draft  
Plant: Holy Basil  
Candidate ID: WSL-0005  
Folder: `research-packs/WSL-0005-holy-basil/`

## Repository sources

### 1. Windowsill production index

URL: https://github.com/DennisHedegreen/windowsill-api/blob/main/plants/index.json

Supports:

- `WSL-0005-holy-basil.json` is the fifth listed production plant file.
- Current production count is 148.
- This pack is an audit of an existing production entry, not a new live plant.

Does not support:

- Botanical correctness.
- Temperature values.
- Edibility or safety.
- Container or climate fit.

### 2. Existing production plant file — WSL-0005 Holy Basil

URL: https://github.com/DennisHedegreen/windowsill-api/blob/main/plants/WSL-0005-holy-basil.json

Supports:

- Existing entry ID: `WSL-0005`.
- Existing English name: `Holy Basil`.
- Existing Danish name: `Hellig Basilikum`.
- Existing candidate Latin name: `Ocimum tenuiflorum`.
- Existing note that the plant is also known as Tulsi.
- Existing values being audited: temperature, sun, context, grow time, hardiness, habit and notes.

Does not support:

- That `species: "basil"` is correct as a taxonomic species field.
- That `max_temp: 40` is appropriate for a Windowsill active-growth recommendation threshold.
- That `hardiness_temp: -1` is appropriate for a frost-sensitive basil relative.
- That the plant has been expert reviewed.

## Botanical / taxonomic sources

### 3. Plants of the World Online — Kew Science, Ocimum tenuiflorum L.

URL: https://powo.science.kew.org/taxon/urn:lsid:ipni.org:names:452874-1

Supports:

- Kew-linked references identify `Ocimum tenuiflorum L.` as a recognised name for Holy Basil/Tulsi.
- The plant is in genus `Ocimum` and family `Lamiaceae`.
- The existing Windowsill `name_latin` is plausible at species level.

Does not support:

- The exact Windowsill numeric model values.
- That all plants sold as "holy basil" are the same species.
- Container or windowsill suitability.

### 4. Wikipedia — Ocimum tenuiflorum

URL: https://en.wikipedia.org/wiki/Ocimum_tenuiflorum

Supports:

- Holy Basil/Tulsi is commonly identified as `Ocimum tenuiflorum`.
- It is an aromatic plant in `Lamiaceae`.
- It is widely cultivated in Southeast Asian tropical contexts and used in Thai and Minangkabau culinary contexts.
- It is culturally/religiously important in Hindu traditions.
- It should not be confused with Thai basil.

Does not support:

- Expert-reviewed Windowsill field values.
- Exact growing thresholds.
- Production-grade safety review.

### 5. Wikipedia — Ocimum

URL: https://en.wikipedia.org/wiki/Ocimum

Supports:

- `Ocimum` includes cooking basil and the medicinal/cultural herb tulsi / holy basil, `O. tenuiflorum`.
- `Ocimum` species are aromatic herbs/shrubs in `Lamiaceae`.

Does not support:

- Exact Windowsill model values.
- Holy-Basil-specific container fit.
- Edibility beyond broad context.

## Growing / climate sources

### 6. The Spruce — How to Grow and Care for Holy Basil

URL: https://www.thespruce.com/holy-basil-plant-profile-5184884

Supports:

- Holy Basil is also known as Tulsi.
- It can refer to `Ocimum tenuiflorum`, and source identity matters because it can be confused with other basil types.
- Holy Basil can be grown in the garden or in containers indoors/outdoors.
- It needs plenty of sunlight, light/airy well-drained soil and steady moisture without soggy conditions.
- It is grown as an annual in cooler regions and as perennial only in warmer climates.
- It prefers warm temperatures and can be grown indoors if conditions are suitable.

Does not support:

- Formal botanical acceptance.
- Universal success on cool northern windowsills.
- Exact Windowsill `grow_time_weeks` or `weeks_from_transplant`.

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

- Holy-Basil-specific accepted botanical naming.
- Exact Holy-Basil-specific temperature thresholds.
- Exact Holy-Basil-specific harvest timing under Windowsill’s locked meaning.

### 8. Iowa State University Extension — Growing Basil in the Home Garden

URL: https://yardandgarden.extension.iastate.edu/how-to/growing-basil-home-garden

Supports:

- Basil is a member of the mint family.
- Basil is tender, cold-sensitive and readily damaged by frost.
- Basil can be grown indoors in a sunny window.
- Basil is well-suited for containers.
- Basil leaves and stems are used fresh and dry in food contexts.

Does not support:

- Holy-Basil-specific botanical naming.
- Exact Windowsill `min_temp`, `max_temp`, `optimal_temp`, `grow_time_weeks` or `weeks_from_transplant`.
- Supplement, extract or health-use safety.

### 9. US Basil Consortium / Rutgers — Growing Basil in a Commercial Setting

URL: https://usbasilconsortium.rutgers.edu/grower-research-resources/grower-resources/growing-basil-in-a-commercial-setting/

Supports:

- Basil requires full sunlight and at least six hours of direct sunlight per day.
- Optimal basil growth temperature range is given as 70–90°F / 21–32°C.
- Basil should be grown in fertile, well-drained soil with good moisture retention.
- Harvest begins once plants reach sufficient size.

Does not support:

- Exact Holy-Basil-specific heat limit.
- Windowsill winter performance.
- Exact first realistic edible harvest timing for Holy Basil.
- Holy Basil taxonomy.

## Safety / scope-boundary sources

### 10. Verywell Health — Holy Basil Benefits: Ayurveda Herbal Medicine

URL: https://www.verywellhealth.com/holy-basil-4766587

Supports:

- Holy Basil is used in traditional medicine and as a culinary herb/tea.
- Research and supplement-use claims are separate from normal food use.
- Supplement forms raise separate safety and interaction questions and should not be treated as covered by a home-growing edible-plant entry.

Does not support:

- Recommending Holy Basil as treatment for any condition.
- Safety of extracts, capsules, high-dose products or long-term supplement use in a Windowsill plant entry.
- Exact home-growing temperature or harvest timing.

## Personal observation

No personal observation was provided for this WSL-0005 audit pack.

## Source quality notes

- Strong current production grounding: existing Windowsill file.
- Stronger botanical review is still needed because direct official source retrieval was limited in this pass.
- Strong practical growing support: The Spruce for Holy-Basil-specific container/indoor care, plus general basil support from UMN, Iowa State and Rutgers.
- Key weak area: exact Holy-Basil-specific temperature and harvest timing.
- Safety boundary is important because Holy Basil is often discussed medicinally; this pack only covers normal culinary leaf/tea use.
