# Audit state — WSL-0003 Lemon Basil

Status: review-ready candidate; no production change proposed yet
Audited: 2026-07-25
Production record: `plants/WSL-0003-lemon-basil.json`
Candidate record: `research-packs/WSL-0003-lemon-basil/plant.json`

## Scope

This audit compares the seeded production record with its candidate workpack.
It does not change the production library, live API or public count.

## Evidence Readback

Kew POWO accepts `Ocimum × africanum Lour.` as the hybrid `O. americanum × O.
basilicum` and treats the current production name `Ocimum × citriodorum Vis.`
as a synonym. This makes the candidate `name_latin` source-supported rather
than merely a secondary-source preference.

General basil authorities support the warm, bright, frost-sensitive and
container-suitable model. They do not establish exact Lemon-Basil cultivar
timing, pot dimensions or universal heat thresholds.

## Candidate Difference Assessment

| Field or area | Current production | Candidate | Audit result |
|---|---|---|---|
| `name_latin` | `Ocimum × citriodorum` | `Ocimum × africanum` | Source-supported correction: Kew accepts the candidate and lists the current value as a synonym. |
| `species` | `basil` | `africanum` | Source-supported hybrid epithet, but the legacy field has no explicit hybrid-rank convention; retain human review of representation. |
| `sun_hours` / `optimal_temp` | `5` / `22` | `6` / `26` | Plausible general-basil model revision; exact Lemon-Basil values still need review. |
| `grow_time_weeks` / `weeks_from_transplant` | `6` / `3` | `7` / `4` | Needs review; sources do not give one universal Lemon-Basil useful-harvest schedule. |
| `hardiness_temp` | `-1` | `0` | Needs review; both are simplified frost-risk boundaries, not direct survival measurements. |
| `habit.note` / `notes` | terse seeded wording | cautious light, warmth, frost and culinary-use wording | Source-aligned wording; review together with context fit. |
| `type` | `hybrid` | `hybrid` | Source-supported hybrid origin; broad commercial cultivar identity remains uncertain. |

## Decision State

```text
evidence_state: source_ready
botanical_name_state: accepted_name_supported_schema_representation_needs_review
human_review_state: not_reviewed
production_state: unchanged
promotion_state: blocked_pending_review
```

The candidate is ready for review. Its accepted hybrid name is supported, but
the API's legacy `species` field and the remaining model estimates must be
reviewed before any production update.

## Next Bounded Action

Record future independent review in `expert_review.md`, then decide separately
whether to update the production record. Do not create keys, send outreach,
change `plants/`, deploy the API or update the live count as part of this audit.
