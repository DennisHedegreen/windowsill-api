# Windowsill Plant Research Backlog

Status values:

- `not_started`
- `source_search`
- `draft_pack_created`
- `needs_human_check`
- `needs_expert_review`
- `ready_for_pr`
- `accepted`
- `rejected_or_removed`

## Current batch

| ID | Plant | File | Risk | Status | Research pack | Notes |
|---|---|---|---|---|---|---|
| WSL-0001 | Genovese Basil | `plants/WSL-0001-genovese-basil.json` | low, with extract/supplement caveat | `draft_pack_created` | `research-packs/WSL-0001-genovese-basil/` | First audit pack. Needs human check before promotion. |

## Next action

Review WSL-0001 manually before moving to WSL-0002.

Checklist:

- Confirm whether `species` should be taxonomic (`basilicum`) or common (`basil`).
- Confirm whether `grow_time_weeks: 8` is the right estimate under the locked meaning: first realistic edible harvest from seed/sowing.
- Confirm whether `hardiness_temp: 0` is the right approximate survival threshold for frost-sensitive basil.
- Decide if safety caveat for essential oil/extract/supplement should be standard for basil-type entries.
