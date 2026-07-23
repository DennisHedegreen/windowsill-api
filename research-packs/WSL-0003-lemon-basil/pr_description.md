# PR description — Add WSL-0003 Lemon Basil research pack

## Summary

This PR adds a research-pack-only audit draft for the existing Windowsill entry:

`plants/WSL-0003-lemon-basil.json`

New research pack folder:

`research-packs/WSL-0003-lemon-basil/`

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

The existing Lemon Basil production entry is plausible, but several values need review before any promotion or correction:

- `name_latin: "Ocimum × citriodorum"` may be better treated as a synonym or horticultural label, with `Ocimum × africanum` as the candidate accepted name.
- `species: "basil"` should probably be changed if the field is taxonomic.
- Existing `sun_hours: 5` is probably too low for a full-sun basil recommendation.
- Existing `optimal_temp: 22` is probably too cool as the main sweet spot for a warm-season basil.
- Existing `grow_time_weeks: 6` and `weeks_from_transplant: 3` are likely optimistic for useful culinary harvest.
- Existing `hardiness_temp: -1` risks implying frost tolerance; this pack uses `0` as a frost-boundary simplification.

## Source summary

Sources used:

- Existing Windowsill `plants/index.json`
- Existing Windowsill `plants/WSL-0003-lemon-basil.json`
- Kew POWO for `Ocimum basilicum` species-level botanical grounding
- Wikipedia Lemon Basil and Limonenbasilikum pages for lemon-basil-specific naming/synonym signals
- Wikipedia Basil page for general basil/hybrid context
- Iowa State University Extension for basil cold sensitivity, containers and windowsill fit
- University of Minnesota Extension for basil light, germination, indoor/container cautions and harvest behaviour
- Rutgers / US Basil Consortium for basil sun and 21–32°C optimal growth range
- The Spruce for lemon-basil gardening/culinary context and naming inconsistency
- BfR for alkenylbenzene safety boundary around basil/herb/extract/supplement contexts

## Uncertainty summary

Key uncertainties:

- Whether Windowsill should use `Ocimum × africanum` or keep `Ocimum × citriodorum`
- How Windowsill should encode hybrid names using the current schema
- Exact active-growth temperature thresholds for Lemon Basil
- Exact `grow_time_weeks` under Windowsill’s locked meaning
- Exact `weeks_from_transplant`
- Safety boundary beyond normal culinary leaf/tender-stem use
- Indoor windowsill reliability under weak winter light

## Human / expert review needed

Before promotion or production correction, reviewers should confirm:

- Preferred Latin naming convention for Lemon Basil
- Whether `name_latin` should remain `Ocimum × citriodorum` or be changed to `Ocimum × africanum`
- Whether `species` should be `africanum` or another hybrid-safe value
- Whether `min_temp: 15`, `max_temp: 33`, `optimal_temp: 26`, `hardiness_temp: 0` and `hardiness_zone_min: 10` are acceptable
- Whether `sun_hours: 6` is the right model value
- Whether `grow_time_weeks: 7` and `weeks_from_transplant: 4` are realistic under the locked field meanings
- Whether the safety note is strong enough without overstating risk

## Review status

Expert review status: not reviewed  
Decision: pending
