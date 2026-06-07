# PR description — Add WSL-0004 Purple Basil research pack

## Summary

This PR adds a research-pack-only audit draft for the existing Windowsill entry:

`plants/WSL-0004-purple-basil.json`

New research pack folder:

`research-packs/WSL-0004-purple-basil/`

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

The existing Purple Basil production entry is plausible, but several values need review before any promotion or correction:

- `name_latin: "Ocimum basilicum 'Purpurascens'"` may be too specific for a broad Purple Basil type-group entry.
- `species: "basil"` should probably be `basilicum` if the field is taxonomic.
- Existing `optimal_temp: 23` is probably too cool as the main sweet spot for a warm-season basil.
- Existing `weeks_from_transplant: 3` is likely optimistic for a useful culinary harvest.
- Existing `hardiness_temp: -1` risks implying frost tolerance; this pack uses `0` as a frost-boundary simplification.
- Existing `type: "op"` is carried forward provisionally but needs confirmation if Windowsill treats type as seed-line strict.

## Source summary

Sources used:

- Existing Windowsill `plants/index.json`
- Existing Windowsill `plants/WSL-0004-purple-basil.json`
- Kew POWO for accepted species-level botanical grounding of `Ocimum basilicum`
- Iowa State University Extension for purple-leaf basil cultivars, culinary use, containers and windowsill fit
- University of Minnesota Extension for basil light, germination, indoor/container cautions and harvest behaviour
- Rutgers / US Basil Consortium for basil sun and 21–32°C optimal growth range
- The Spruce for purple-basil gardening/culinary context
- Wikipedia cultivar pages as weak secondary naming signals only
- BfR for general basil/source-boundary safety caution

## Uncertainty summary

Key uncertainties:

- Whether Windowsill should keep a broad Purple Basil entry or split into cultivar-specific entries
- Whether `name_latin` should be `Ocimum basilicum`, `Ocimum basilicum 'Purpurascens'`, or another cultivar-specific label
- Exact active-growth temperature thresholds for Purple Basil
- Exact `grow_time_weeks` under Windowsill’s locked meaning
- Exact `weeks_from_transplant`
- Whether `type: "op"` is defensible for a broad type-group entry
- Indoor windowsill reliability and colour quality under weak winter light

## Human / expert review needed

Before promotion or production correction, reviewers should confirm:

- Preferred Latin naming convention for Purple Basil
- Whether the broad type-group entry should stay broad or become cultivar-specific
- Whether `species` should be `basilicum`
- Whether `min_temp: 15`, `max_temp: 33`, `optimal_temp: 26`, `hardiness_temp: 0` and `hardiness_zone_min: 10` are acceptable
- Whether `grow_time_weeks: 7` and `weeks_from_transplant: 4` are realistic under the locked field meanings
- Whether `type: "op"` is defensible
- Whether the safety boundary is clear enough without overstating risk

## Review status

Expert review status: not reviewed  
Decision: pending
