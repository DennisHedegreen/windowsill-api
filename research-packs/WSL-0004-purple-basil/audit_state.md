# Audit state — WSL-0004 Purple Basil

Status: review-ready candidate; no production change proposed yet
Audited: 2026-07-25
Production record: `plants/WSL-0004-purple-basil.json`
Candidate record: `research-packs/WSL-0004-purple-basil/plant.json`

## Scope

This audit compares the seeded production record with its candidate workpack.
It does not change production data, the live API or the public plant count.

## Evidence Readback

Kew POWO accepts `Ocimum basilicum L.` at species level. Iowa State Extension
describes purple-leaf basil as several culinary and ornamental cultivars, not
one universal Purple Basil cultivar. This supports the candidate's conservative
species-level name and makes the current `Purpurascens` label a naming decision
rather than a settled generic identity.

General basil authorities support the warm, bright, frost-sensitive and
container-suitable model. They do not establish one exact Purple-Basil cultivar
profile for timing, colour or heat response.

## Candidate Difference Assessment

| Field or area | Current production | Candidate | Audit result |
|---|---|---|---|
| `name_latin` | `Ocimum basilicum 'Purpurascens'` | `Ocimum basilicum` | Conservative species-level grounding for a broad type-group entry; human review must decide whether to keep one broad entry or split cultivars. |
| `species` | `basil` | `basilicum` | Source-supported taxonomic-epithet correction. |
| `max_temp` / `optimal_temp` | `34` / `23` | `33` / `26` | Plausible general-basil model revision; not cultivar-specific trial evidence. |
| `weeks_from_transplant` | `3` | `4` | Needs review; the useful-harvest estimate varies by named cultivar and conditions. |
| `hardiness_temp` | `-1` | `0` | Needs review; both are simplified frost-boundary models, not direct survival measurements. |
| `habit.note` / `notes` | terse seeded wording | cautious light, colour, frost and culinary-use wording | Source-aligned wording; review with the broad-entry decision. |
| `type` | `op` | `op` | Unresolved for a broad type group; do not infer seed genetics from leaf colour. |

## Decision State

```text
evidence_state: source_ready
botanical_name_state: species_supported_broad_type_scope_needs_review
human_review_state: not_reviewed
production_state: unchanged
promotion_state: blocked_pending_review
```

The candidate is ready for review. The immediate decision is not whether purple
basil exists, but whether Windowsill should keep a broad, explicitly
species-level type entry or represent named cultivars separately.

## Next Bounded Action

Record future independent review in `expert_review.md`, then make a separate
promotion decision. Do not create keys, send outreach, change `plants/`, deploy
the API or update the live count as part of this audit.
