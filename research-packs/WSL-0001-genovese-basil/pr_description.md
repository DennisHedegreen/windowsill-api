# PR description — Add research/audit pack for WSL-0001 Genovese Basil

## Summary

This PR adds a research/audit pack for the existing Windowsill plant entry:

```text
plants/WSL-0001-genovese-basil.json
```

Pack folder:

```text
research-packs/WSL-0001-genovese-basil/
```

Required files included:

- `plant.json`
- `source_registry.md`
- `field_rationale.md`
- `uncertainty_notes.md`
- `expert_review.md`
- `pr_description.md`

## What changed compared with the existing entry

Suggested candidate changes in `plant.json`:

- `species`: changed from `basil` to `basilicum` if the field is meant taxonomically.
- `max_temp`: changed from `35` to `32` as active-growth comfort max.
- `optimal_temp`: changed from `24` to `26` as a midpoint in the supported optimum range.
- `grow_time_weeks`: changed from `6` to `8` as a less optimistic first-useful-harvest model.
- `weeks_from_transplant`: changed from `3` to `5`.
- `hardiness_temp`: changed from `-1` to `0`, with warning that basil is frost-sensitive and should not be treated as frost-hardy.
- Added `expert_review` default object.
- Added audit/safety wording around normal culinary use versus essential oils, extracts, supplements and medicinal dosing.

## Sources used

Main sources:

- Kew POWO — `Ocimum basilicum L.` accepted species.
- Royal Botanic Gardens, Kew — windowsill basil growing, Lamiaceae, leaves/flowers edible, warm full-sun conditions.
- University of Minnesota Extension — 6–8 hours light, well-drained soil, tender annual, germination and indoor-light guidance.
- Iowa State University Extension — frost sensitivity, container/window growing, outdoor planting after cold risk.
- US Basil Consortium / Rutgers — six hours direct sun, optimal growth range 21–32°C.
- De Bolster — Genovese-specific seed listing, `Ocimum basilicum`, low-growing annual, 20 × 20 cm spacing, 20–50 cm height, sun, water/warmth/nutrition.
- Johnny's Selected Seeds — Genovese basil days to maturity and germination timing.
- PanAmerican Seed — Genovese-type pot/transplant timing support, but cultivar-specific.
- BfR and Wageningen/Food and Chemical Toxicology summary — safety boundary for alkenylbenzenes, flavour use versus supplements/extracts.

## Uncertainty

Still uncertain:

- Whether Windowsill should store `Ocimum basilicum 'Genovese'` as the Latin name or split species and cultivar/type.
- Whether `grow_time_weeks` should mean first edible leaves, first useful harvest or full maturity.
- Whether `hardiness_temp` should model plant death, active outdoor suitability or protected survival.
- Whether the current `type: op` is broadly safe for the generic Genovese entry or only source-specific.

## Expert review

This pack is not expert reviewed.

The `expert_review` object is included with:

```text
status: not_reviewed
model: three_independent_reviewers_per_plant
reviewers_required: 3
reviews: []
decision: pending
```

## Suggested status after merge

```text
needs_human_check
```

Do not promote final values into production without human review.
