# Contributing to Windowsill

The Windowsill plant library is open. If you know a plant variety that is missing, you can add it via GitHub pull request.

Windowsill welcomes both human-only and AI-assisted contributions. AI can help with research, structure and drafting, but contributors are responsible for checking the data and stating uncertainty clearly.

If you want the easiest path, start with [Add a plant with ChatGPT](docs/CHATGPT_PLANT_RESEARCH_GUIDE.md).

For the fuller AI-assisted workflow, see [docs/AI_PLANT_WORKFLOW.md](docs/AI_PLANT_WORKFLOW.md).

For the exact merge format, see [docs/RESEARCH_PACK_CONTRACT.md](docs/RESEARCH_PACK_CONTRACT.md) and [docs/GITFLOW.md](docs/GITFLOW.md).

## What we need

Each plant variety is one JSON file. A good contribution has accurate climate data — specifically `min_temp`, `optimal_temp`, `hardiness_temp`, and `sun_hours`. These are the values the scoring model depends on.

If you are not sure about a value, make a reasonable estimate and note it in `contributor_note`. Uncertain data with a note is better than no data. Corrections to existing plants are equally welcome.

## How to contribute

New plants should normally start as a research pack, not as a direct plant-library entry.

1. Fork this repository or create a branch if you have write access
2. Create one folder under `research-packs/`
3. Use the exact required files from `research-packs/_template/`
4. Run `python3 scripts/validate_research_packs.py`
5. Open a pull request — include your data sources and uncertainty notes in the PR description
6. Promote into `plants/` only after review

## AI-assisted contributions

If you use an AI tool to help add a plant, do not ask it to simply "make a plant JSON".

Ask it to prepare a small research-backed work pack:

```text
plant.json
source_registry.md
field_rationale.md
uncertainty_notes.md
expert_review.md
pr_description.md
```

Use `research-packs/_template/` if you want files to copy.

Pull requests that add research packs are checked by GitHub Actions. The validator only accepts the required folder/file structure and controlled values.

At minimum, the AI-assisted work should check:

- accepted botanical name, family and genus
- whether the plant is native, introduced, cultivated or only culturally associated with the region
- active growth temperature, optimal temperature, heat limit and survival/hardiness temperature
- sun requirement and container suitability
- growth habit: compact herb, vine, shrub, tree, tuber crop, cactus, etc.
- food safety concerns
- whether the plant realistically fits `windowsill`, `balcony` or `garden`

Use the starter prompt and source hierarchy in [docs/AI_PLANT_WORKFLOW.md](docs/AI_PLANT_WORKFLOW.md) when preparing AI-assisted plant contributions.

## Plant file template

```json
{
  "id": "WSL-0149",
  "contributor": "your-github-handle",
  "contributor_note": "Source: RHS Plant Finder / personal observation / etc.",
  "name_en": "Plant Variety Name",
  "name_da": "Dansk Navn",
  "name_latin": "Genus species 'Cultivar'",
  "family": "Familyaceae",
  "genus": "Genus",
  "species": "species-slug",
  "type": "op",
  "min_temp": 5,
  "max_temp": 30,
  "optimal_temp": 18,
  "sun_hours": 5,
  "sun_direct": "full",
  "context": ["windowsill", "balcony", "garden"],
  "grow_time_weeks": 8,
  "weeks_from_transplant": 5,
  "hardiness_temp": -10,
  "hardiness_zone_min": 9,
  "habit": {
    "windowsill": "good",
    "balcony": "good",
    "garden": "good",
    "note": "Any specific growing notes for containers or open ground."
  },
  "notes": "General growing notes. Culinary use. Any special requirements."
}
```

## Field guide

| Field | Notes |
|---|---|
| `type` | `op` = open-pollinated, `heirloom`, `hybrid` |
| `min_temp` | Practical lower threshold for active growth or realistic recommendation. Not the survival minimum. |
| `optimal_temp` | Practical growth sweet spot. |
| `max_temp` | Practical upper threshold before heat stress or quality problems become likely. |
| `grow_time_weeks` | Estimated weeks from seed/sowing to first realistic edible harvest, not biological maturity. |
| `weeks_from_transplant` | Estimated weeks from transplanting or buying a young plant to first realistic edible harvest. |
| `hardiness_temp` | Approximate survival threshold or overwinter tolerance. Use RHS H-rating or USDA zone data. Different from `min_temp`. |
| `hardiness_zone_min` | Derive from `hardiness_temp` — see USDA table in [REFERENCE.md](REFERENCE.md#usda-zone-from-hardiness_temp) |
| `sun_direct` | `full` = needs direct sun · `partial` = tolerates partial shade · `shade` = prefers shade |
| `context` | Only include contexts where the plant can realistically succeed |
| `habit` values | `good` · `acceptable` · `risky` · `unsuitable` |

Do not add `maturity_weeks` yet. If a plant is cut-and-come-again or has ongoing harvest behaviour, explain it in `notes` and the research pack rationale.

## Safety flags

If a plant has culinary safety concerns, include one of these exact phrases in `notes`:

```text
"Toxic in large quantities — not for culinary use."
"Phototoxic sap — handle with gloves."
"Internal use restricted due to alkaloids."
```

The API scans these phrases automatically and applies a score penalty.

## Questions

Open an issue or email api@windowsill.dk
