# AI-assisted plant contribution workflow

Windowsill accepts plant data contributions through pull requests. AI tools may help with research, structure, drafting and formatting, but they must not be treated as authorities.

The goal is not to add as many plants as possible. The goal is to add plants with traceable reasoning, realistic growing contexts and clear uncertainty notes.

If you want the easiest public-facing version first, use [Add a plant with ChatGPT](CHATGPT_PLANT_RESEARCH_GUIDE.md).

---

## Core principle

AI can help prepare a contribution. A human contributor is still responsible for checking whether the data makes sense.

A good AI-assisted plant contribution should answer these questions:

1. What plant is this, botanically?
2. Is the name accepted, ambiguous, local, commercial or outdated?
3. Is the plant native to the claimed region, introduced there, cultivated there, or only culturally associated with it?
4. Can the plant realistically grow in a windowsill, balcony or garden context?
5. What temperatures, sun needs, hardiness and growth habit should the scoring model use?
6. What is uncertain?
7. What sources support the values?

---

## Source hierarchy

Use multiple sources when possible. Prefer sources that explain their own basis.

### 1. Botanical authority

Use for accepted names, families, genera, synonyms and native/introduced range.

Examples:

- Kew Plants of the World Online (POWO)
- GRIN / USDA Germplasm Resources Information Network
- national botanical databases
- herbarium or botanical garden references

### 2. Horticultural authority

Use for growing conditions, hardiness, sun, containers, propagation and practical cultivation.

Examples:

- RHS
- university extension services
- botanical garden growing guides
- specialist horticultural societies

### 3. Crop and agronomy sources

Use for food crops, traditional crops, field crops, tuber crops, grain crops and yield/season behaviour.

Examples:

- FAO
- CGIAR / CIP
- university agronomy papers
- agricultural extension PDFs

### 4. Cultural and culinary sources

Use for regional names, food use and cultural relevance. These sources are useful, but they should not override botanical or horticultural evidence.

Examples:

- Slow Food Ark of Taste
- national food/crop institutions
- regional culinary references
- ethnobotanical literature

### 5. Personal observation

Personal growing notes are valuable, especially for windowsill and balcony behaviour. But personal observation should not be the only source for hardiness, toxicity, native range or broad climate limits.

Use personal observation for:

- pot size
- location
- orientation
- light source
- sowing date
- germination time
- first harvest
- failure notes
- local climate/microclimate notes

---

## Recommended AI starter prompt

Copy this prompt into your AI tool and replace the bracketed parts.

```text
You are helping me prepare one plant research pack for the Windowsill API plant library.

Goal:
Create one research pack following docs/RESEARCH_PACK_CONTRACT.md.

Plant:
[COMMON NAME]
[COUNTRY / REGION CONTEXT]
[KNOWN LATIN NAME, if any]

Repository rules:
- One plant = one research pack folder under research-packs/
- Use WSL-XXXX as placeholder ID unless the maintainer gives you a real ID
- Do not update plants/ or plants/index.json
- Production plant promotion happens later after review
- Do not invent facts
- Mark uncertain values in contributor_note
- Only include contexts where the plant can realistically succeed: windowsill, balcony, garden
- Do not add new schema fields
- Do not add maturity_weeks

Research requirements:
1. Verify accepted botanical name, family and genus.
2. Check whether the plant is native, introduced, cultivated, or only culturally associated with the region.
3. Find active growth temperature, optimal temperature, heat limit and survival/hardiness temperature.
4. Find sun requirement and container suitability.
5. Check growth habit: compact herb, vine, shrub, tree, tuber crop, cactus, etc.
6. Check food safety concerns.
7. Decide whether the plant should be recommended for windowsill, balcony, garden, or suppressed from one or more contexts.
8. Produce the six required research-pack files:
   - plant.json
   - source_registry.md
   - field_rationale.md
   - uncertainty_notes.md
   - expert_review.md
   - pr_description.md
```

---

## Recommended work pack

For serious contributions, prepare a small work pack before opening the pull request.

Suggested files:

```text
plant.json
source_registry.md
field_rationale.md
uncertainty_notes.md
pr_description.md
```

### plant.json

The final plant file that will go into `plants/`.

### source_registry.md

A list of the sources used, with one short sentence explaining what each source supports.

Example:

```text
Kew POWO — accepted botanical name, family and distribution.
RHS — hardiness and container guidance.
University extension guide — temperature, sun and harvest timing.
Personal observation — balcony performance in Copenhagen, summer 2026.
```

### field_rationale.md

A short explanation for the modelling choices.

Include why the plant is or is not suitable for:

- windowsill
- balcony
- garden

### uncertainty_notes.md

List open questions or weak values.

Examples:

```text
hardiness_temp is estimated from zone guidance, not a direct crop trial.
max_temp is based on pepper-family extension guidance, not this cultivar specifically.
Native range is uncertain because sources disagree between accepted taxonomy and culinary usage.
```

### pr_description.md

A ready-to-paste pull request description.

---

## Context decision rules

Do not add all contexts by default.

### windowsill

Use only when the plant can realistically grow in a normal indoor window or small indoor container.

Good signs:

- compact habit
- tolerates indoor light or filtered light
- useful harvest from leaves or small fruits
- does not require a huge root volume

Bad signs:

- large vine
- tree or palm
- long-season tuber crop
- grain crop grown for seed
- requires outdoor pollination or large trellis

### balcony

Use when the plant can work in a pot, grow bag or container outdoors.

Good signs:

- container tolerant
- benefits from outdoor light
- can be protected from frost
- manageable size with pruning or support

### garden

Use when the plant needs open ground, larger soil volume, trellis, long season or more stable outdoor conditions.

---

## Safety and honesty rules

Do not hide uncertainty.

Use `contributor_note` to mark weak data. Use `notes` to explain safety concerns or special handling.

Never casually recommend a plant as edible if normal preparation is important for safety.

Examples that need caution:

- cassava / yuca
- tarwi / lupin
- plants with phototoxic sap
- plants with restricted internal use
- plants where only specific parts are edible

---

## Pull request checklist

Before opening a PR:

- [ ] The pack is in `research-packs/WSL-XXXX-plant-name/`
- [ ] The six required research-pack files are present
- [ ] `plant.json` is valid JSON
- [ ] No unsupported schema fields are added
- [ ] The plant has realistic context values
- [ ] Sources are listed in `source_registry.md` and the PR description
- [ ] Uncertainty is stated clearly
- [ ] No unsupported claims are presented as facts
- [ ] The pack does not claim expert review unless real reviewer notes exist
- [ ] The PR says whether it is research-pack only or a production promotion

---

## What AI should not do

AI should not:

- invent citations
- invent exact temperatures when sources are weak
- treat all regional food plants as native plants
- add trees and palms as normal windowsill crops
- assume all edible plants are safe without preparation notes
- treat personal observation as universal evidence
- optimize for plant count over data quality

Windowsill is more useful when it is slower, traceable and honest.
