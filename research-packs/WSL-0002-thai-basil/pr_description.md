# PR description — Add WSL-0002 Thai Basil research pack

## Summary

This PR adds a research-pack-only audit draft for the existing Windowsill entry:

`plants/WSL-0002-thai-basil.json`

New research pack folder:

`research-packs/WSL-0002-thai-basil/`

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

The existing Thai Basil production entry is broadly plausible, but several values need review before any promotion or correction:

- `species: "basil"` should probably be `basilicum` if the field is taxonomic.
- `name_latin: "Ocimum basilicum var. thyrsiflora"` is useful as a horticultural label, but botanical acceptance is uncertain because Kew POWO supports `Ocimum basilicum L.` at species level and does not list `var. thyrsiflora` among accepted infraspecifics.
- Existing `max_temp: 38` is likely too optimistic for a practical Windowsill active-growth / quality threshold.
- Existing `hardiness_temp: -1` risks implying frost tolerance; this pack uses `0` as a frost-boundary simplification.
- `type: "op"` is carried forward provisionally but needs confirmation if Windowsill treats type as seed-genetics strict.

## Source summary

Sources used:

- Existing Windowsill `plants/index.json`
- Existing Windowsill `plants/WSL-0002-thai-basil.json`
- Kew POWO for accepted species-level botanical grounding
- Iowa State University Extension for Thai basil identity, morphology, cold sensitivity, containers and windowsill fit
- University of Minnesota Extension for basil light, germination, indoor/container cautions and harvest behaviour
- Rutgers / US Basil Consortium for basil sun and 21–32°C optimal growth range
- The Spruce for Thai-basil-specific home-growing notes, USDA zones and seven-week harvest estimate
- BfR for alkenylbenzene safety boundary around basil/herb/extract/supplement contexts

## Uncertainty summary

Key uncertainties:

- Botanical naming of `Ocimum basilicum var. thyrsiflora`
- Exact active-growth temperature thresholds for Thai basil
- Exact `grow_time_weeks` under Windowsill’s locked meaning
- Exact `weeks_from_transplant`
- Whether `type: "op"` should be retained
- Safety boundary beyond normal culinary leaf/tender-stem use
- Indoor windowsill reliability under weak winter light

## Human / expert review needed

Before promotion or production correction, reviewers should confirm:

- Preferred Latin naming convention for Thai Basil
- Whether `species` should be `basilicum`
- Whether `name_latin` should remain `Ocimum basilicum var. thyrsiflora` or be simplified to `Ocimum basilicum`
- Whether `min_temp: 18`, `max_temp: 34`, `optimal_temp: 27`, `hardiness_temp: 0` and `hardiness_zone_min: 10` are acceptable
- Whether `grow_time_weeks: 7` and `weeks_from_transplant: 4` are realistic under the locked field meanings
- Whether `type: "op"` is defensible
- Whether the safety note is strong enough without overstating risk

## Review status

Expert review status: not reviewed  
Decision: pending
