# Audit state — WSL-0005 Holy Basil

Status: review-ready candidate; no production change proposed yet
Audited: 2026-07-25
Production record: `plants/WSL-0005-holy-basil.json`
Candidate record: `research-packs/WSL-0005-holy-basil/plant.json`

## Scope

This audit compares the seeded production record with its candidate workpack.
It does not change the production library, live API or public count.

## Evidence Readback

Kew POWO accepts `Ocimum tenuiflorum L.` and treats `Ocimum sanctum L.` as a
synonym. This supports the candidate species epithet and gives a clear rule for
normalizing an older or commercial `O. sanctum` label.

Practical gardening sources support a warm, frost-sensitive plant that can grow
in containers where there is sufficient warmth and light. They do not establish
one exact Holy-Basil harvest schedule, pot size or upper temperature limit for
Windowsill's model.

The candidate explicitly limits edible-use wording to ordinary culinary leaves
and tea. It makes no treatment, supplement, extract, essential-oil or health
claim.

## Candidate Difference Assessment

| Field or area | Current production | Candidate | Audit result |
|---|---|---|---|
| `name_latin` / `species` | `Ocimum tenuiflorum` / `basil` | `Ocimum tenuiflorum` / `tenuiflorum` | Accepted name and epithet are source-supported; `Ocimum sanctum` is a synonym, not a separate species record. |
| `max_temp` | `40` | `34` | Plausible warm-basil model revision, but not Holy-Basil-specific trial evidence; needs review. |
| `hardiness_temp` | `-1` | `0` | Needs review; both are simplified frost-boundary models, while sources establish frost sensitivity rather than a direct survival threshold. |
| `habit.note` / `notes` | terse seeded wording, including an Ayurvedic-use reference | cautious warmth, culinary/tea and no-health-claim wording | Source-aligned scope boundary; retain this boundary regardless of later model decisions. |
| `type` | `op` | `op` | Unresolved; a commercial seed-line claim needs evidence before it becomes a genetic classification. |
| `grow_time_weeks` / `weeks_from_transplant` | `8` / `4` | `8` / `4` | Retained estimate; sources do not verify a universal useful-harvest schedule. |

## Decision State

```text
evidence_state: source_ready
botanical_name_state: accepted_name_and_synonym_supported
safety_scope_state: culinary_and_tea_only_no_health_claims
human_review_state: not_reviewed
production_state: unchanged
promotion_state: blocked_pending_review
```

The candidate is ready for review. The remaining decision concerns the numeric
model estimates and seed-line representation, not the accepted botanical name.

## Next Bounded Action

Record future independent review in `expert_review.md`, then make a separate
promotion decision. Do not create keys, send outreach, change `plants/`, deploy
the API or update the live count as part of this audit.
