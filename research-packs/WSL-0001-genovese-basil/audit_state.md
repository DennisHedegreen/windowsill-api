# Audit state — WSL-0001 Genovese Basil

Status: review-ready candidate; no production change proposed yet
Audited: 2026-07-25
Production record: `plants/WSL-0001-genovese-basil.json`
Candidate record: `research-packs/WSL-0001-genovese-basil/plant.json`

## Scope

This audit compares the existing seeded production record with the candidate
workpack. It does not treat the workpack as an expert review and does not
change the live API or the production library.

## Evidence Readback

The source registry was checked again on 2026-07-25 against the principal
source classes.

- Kew POWO accepts `Ocimum basilicum L.` and places it in `Ocimum` /
  Lamiaceae. This supports correcting the API `species` value from the
  common-name fragment `basil` to the taxonomic epithet `basilicum`.
- University of Minnesota Extension supports basil as a tender culinary annual,
  six to eight hours of bright light, drainage and the limitation of indoor
  winter light.
- Iowa State University Extension supports frost sensitivity, sunny-window and
  container suitability, with outdoor planting only after frost risk.
- The US Basil Consortium supports full sun and an optimum growth interval of
  21–32 °C. It is not Genovese-specific experimental proof for every model
  number.

The source registry remains the detailed source-of-record, including its
explicit limits for cultivar identity, timing and concentrated-extract safety.

## Candidate Difference Assessment

| Field or area | Current production | Candidate | Audit result |
|---|---|---|---|
| `species` | `basil` | `basilicum` | Source-supported correction; retain the current `name_latin` caveat about Genovese identity. |
| `max_temp` / `optimal_temp` | `35` / `24` | `32` / `26` | Plausible model revision from the 21–32 °C horticultural range; needs review because the API compresses varied growing conditions into two values. |
| `grow_time_weeks` | `6` | `8` | Needs review; useful harvest timing varies by cultivar, starting method and light. |
| `weeks_from_transplant` | `3` | `5` | Needs review; candidate sources are not one universal Genovese trial. |
| `hardiness_temp` | `-1` | `0` | Needs review; both values are simplified frost-risk boundaries, not a measured hardy-survival claim. |
| `habit.note` / `notes` | terse seeded wording | cautious light, airflow, frost and culinary-use wording | Source-aligned wording; review it with the climate/context decision. |
| `contributor_note` | generic source warning | explicit audit limitations | Source-aligned provenance improvement. |
| `type` | `op` | `op` | Unresolved. Current generic Genovese identity may not justify a universal open-pollinated claim. No silent retention decision. |

## Decision State

```text
evidence_state: source_ready
human_review_state: not_reviewed
production_state: unchanged
promotion_state: blocked_pending_review
```

The candidate is ready for the existing three-reviewer lane. It is not ready
for production promotion because no real independent reviews have been
recorded and the timing, hardiness and generic-type questions remain open.

## Next Bounded Action

Use this exact pack for the approved Genovese reviewer batch. Record replies
in `expert_review.md`; then make a separate, explicit promotion decision.

Do not create keys, send outreach, change `plants/`, deploy the API or update
the live count as part of this audit.
