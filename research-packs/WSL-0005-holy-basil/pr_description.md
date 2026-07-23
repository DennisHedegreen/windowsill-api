# PR description — Add WSL-0005 Holy Basil research pack

## Summary

This PR adds a research-pack-only audit draft for the existing Windowsill entry:

`plants/WSL-0005-holy-basil.json`

New research pack folder:

`research-packs/WSL-0005-holy-basil/`

This does not promote the plant, does not add a new production plant, and does not change the live plant count.

## Scope

Included:

- `plant.json`
- `source_registry.md`
- `field_rationale.md`
- `uncertainty_notes.md`
- `expert_review.md`
- `pr_description.md`

Not included:

- No changes to `plants/`
- No changes to `plants/index.json`
- No production count change
- No schema expansion
- No `maturity_weeks`
- No expert-review claim

## Main audit findings

The existing Holy Basil production entry is plausible, but several values need review before any promotion or correction:

- `name_latin: "Ocimum tenuiflorum"` is retained, but synonym/trade confusion with `Ocimum sanctum` and other `Ocimum` species should be reviewed.
- `species: "basil"` should probably be `tenuiflorum` if the field is taxonomic.
- Existing `max_temp: 40` is too high for a practical active-growth / quality recommendation threshold.
- Existing `hardiness_temp: -1` risks implying frost tolerance; this pack uses `0` as a frost-boundary simplification.
- Existing notes mention Ayurvedic use; the research pack narrows scope to normal culinary leaf/tea use and explicitly excludes health claims.

## Source summary

Sources used:

- Existing Windowsill `plants/index.json`
- Existing Windowsill `plants/WSL-0005-holy-basil.json`
- Kew-linked `Ocimum tenuiflorum` botanical references
- Wikipedia `Ocimum tenuiflorum` and `Ocimum` pages as secondary naming/cultural/culinary signals
- The Spruce for Holy-Basil-specific indoor/container growing context
- University of Minnesota Extension for basil light, germination, indoor/container cautions and harvest behaviour
- Iowa State University Extension for basil cold sensitivity, containers and windowsill fit
- Rutgers / US Basil Consortium for basil sun and 21–32°C optimal growth range
- Verywell Health as a boundary source for separating supplement/health-use contexts from Windowsill food-use scope

## Uncertainty summary

Key uncertainties:

- Preferred Latin name and synonym handling: `Ocimum tenuiflorum` vs `Ocimum sanctum`
- Whether all plants sold as Holy Basil/Tulsi are correctly identified
- Exact active-growth temperature thresholds for Holy Basil
- Whether `max_temp: 34` is the right correction from existing `40`
- Exact `grow_time_weeks` under Windowsill’s locked meaning
- Exact `weeks_from_transplant`
- Whether `type: "op"` is defensible for available seed lines
- Indoor windowsill reliability under weak northern winter light
- Safety boundary beyond normal culinary leaf/tea-style use

## Human / expert review needed

Before promotion or production correction, reviewers should confirm:

- Preferred Latin naming convention for Holy Basil / Tulsi
- Whether `species` should be `tenuiflorum`
- Whether `min_temp: 18`, `max_temp: 34`, `optimal_temp: 28`, `hardiness_temp: 0` and `hardiness_zone_min: 10` are acceptable
- Whether `grow_time_weeks: 8` and `weeks_from_transplant: 4` are realistic under the locked field meanings
- Whether `type: "op"` is defensible
- Whether Windowsill production copy should mention cultural context while avoiding health-use endorsement

## Review status

Expert review status: not reviewed  
Decision: pending
