# Audit state — WSL-0002 Thai Basil

Status: review-ready candidate; no production change proposed yet
Audited: 2026-07-25
Production record: `plants/WSL-0002-thai-basil.json`
Candidate record: `research-packs/WSL-0002-thai-basil/plant.json`

## Scope

This audit compares the seeded production record with its candidate workpack.
It does not decide botanical rank by itself, count as expert review, alter the
production library or change the live API.

## Evidence Readback

The principal source classes were rechecked on 2026-07-25.

- Kew POWO accepts `Ocimum basilicum L.` in `Ocimum` / Lamiaceae. Its accepted
  infraspecific list contains `var. basilicum` and `var. minimum`, not
  `var. thyrsiflora`.
- Iowa State University Extension uses `Ocimum basilicum var. thyrsiflora` for
  Thai basil in practical horticultural guidance. It also supports narrow
  leaves, purple stems, anise/licorice-like flavour, frost sensitivity,
  container fit and a sunny windowsill.
- University of Minnesota Extension supports basil as a tender culinary annual
  needing bright light, drainage and added indoor light in darker periods.
- The US Basil Consortium supports full sun and a general basil optimum of
  21–32 °C. It does not establish Thai-basil-specific model thresholds.

The practical Thai-basil name is therefore useful but not settled as an
accepted botanical infraspecific rank. The detailed source limits remain in
`source_registry.md`.

## Candidate Difference Assessment

| Field or area | Current production | Candidate | Audit result |
|---|---|---|---|
| `species` | `basil` | `basilicum` | Source-supported correction if the field stores a taxonomic epithet. |
| `name_latin` | `Ocimum basilicum var. thyrsiflora` | unchanged | Keep only as a practical horticultural label pending botanical review; do not represent it as Kew-accepted rank. |
| `max_temp` | `38` | `34` | Plausible quality-threshold revision, but needs review because 21–32 °C is general basil guidance rather than Thai-basil-specific heat-trial evidence. |
| `hardiness_temp` | `-1` | `0` | Needs review; both values are simplified frost-boundary models, not direct survival measurements. |
| `habit.note` / `notes` | terse seeded wording | cautious light, warmth, frost and culinary-use wording | Source-aligned wording; review it with the context decision. |
| `contributor_note` | generic source warning | explicit audit limitations | Source-aligned provenance improvement. |
| `type` | `op` | `op` | Unresolved. The generic Thai-basil entry is not enough to establish universal open-pollinated status. |
| harvest timing | `7` / `4` weeks | unchanged | Retain only as model estimates. The seed-to-harvest estimate has limited support; transplant timing lacks a direct Thai-basil source. |

## Decision State

```text
evidence_state: source_ready
botanical_name_state: needs_human_review
human_review_state: not_reviewed
production_state: unchanged
promotion_state: blocked_pending_review
```

This pack is ready for targeted review, especially on naming convention,
temperature thresholds and whether the generic `type` field remains defensible.
No production field should be changed merely because the candidate is better
documented than the seeded record.

## Next Bounded Action

Use this pack in a Thai-basil-specific review lane after the Genovese lane has
an approved recipient/key/send decision. Record real review input in
`expert_review.md`, then make a separate promotion decision.

Do not create keys, send outreach, change `plants/`, deploy the API or update
the live count as part of this audit.
