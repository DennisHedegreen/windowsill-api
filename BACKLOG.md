# Windowsill Backlog

Status: active planning queue
Updated: 2026-07-25

Purpose: hold the work needed to make plant data more trustworthy without
mixing research, promotion, deployment and outreach into one action.

This is the data-quality and operations backlog. Product features remain in
`ROADMAP.md`.

## Current Truth

- Live API: healthy, 148 production plants.
- Production records: consistent technical schema, but no structured source or
  expert-review fields.
- Research layer: 5 valid linked workpacks, all pending human review and
  promotion decision.
- GitHub PR queue: empty when checked on 2026-07-25.

## Now — Establish An Honest Audit Queue

| ID | Item | Done when | Gate |
|---|---|---|---|
| WSL-BL-001 | Adopt Plant Data Standard v1 | The production/workpack/decision boundary is written and linked from the operating docs. | Documentation only — no live change. |
| WSL-BL-002 | Create a machine-readable audit inventory for all 148 production IDs | Every ID has an explicit audit state, priority and linked-workpack reference when one exists. | Local data artifact; do not invent audit results. |
| WSL-BL-003 | Reconcile the five existing basil workpacks against their production records | Each candidate diff is listed as `no change`, `needs review` or `promotion proposal`; no values are copied silently. | Human decision before production modification. |
| WSL-BL-004 | Define a risk-first audit order for the remaining baseline library | The queue prioritizes safety, taxonomic ambiguity, climate sensitivity and likely public use over plant count. | No bulk migration. |
| WSL-BL-005 | Use GitHub as the required change-record gate for plant work | `docs/GITFLOW.md`, PR template and weekly guide distinguish research, audit, promotion and deployment PR classes. | Process design only; commit, push and PR creation remain intentional actions. |

## Review Lane — Genovese Basil First

Progress: WSL-0001 through WSL-0005 have evidence-checked `audit_state.md`
files and are review-ready. No candidate has been promoted to production.

| ID | Item | Done when | Gate |
|---|---|---|---|
| WSL-BL-010 | Approve a 3–5 person first reviewer batch | Named recipients are selected from the existing candidate pool and the draft is checked. | Dennis approves recipients. |
| WSL-BL-011 | Create only the required reviewer keys and prepare/send the batch | Each key has a known recipient, expiry/revocation plan and ledger entry. | Explicit approval before creating keys or sending. |
| WSL-BL-012 | Map each received review back to the Genovese workpack | Reviewer input is retained as evidence, agreement/disagreement is recorded, and status stays honest. | No production promotion by absence of replies. |
| WSL-BL-013 | Make a Genovese promotion decision | Decision records accepted corrections, disagreements, cautious wording and remaining uncertainty. | Minimum review gate, then separate production/deploy approval. |

## Data Contract — Design Before Migration

| ID | Item | Done when | Gate |
|---|---|---|---|
| WSL-BL-019 | Collect passive vNext plant-preference profiles inside audited workpacks | Each worked plant records only source-backed light, container, water and establishment preferences, with unknowns retained. | Workpack-only; no API, score or location-model change. |
| WSL-BL-020 | Design a versioned public provenance/review representation | A small schema proposal explains which source/review status may enter API data and how it remains linked to the workpack. | Design review; no API schema change yet. |
| WSL-BL-021 | Add a production-to-API mirror consistency check | A deterministic local check fails when `plants/` and `api/plants/` differ. | Test only; no deployment. |
| WSL-BL-022 | Trial the approved schema on one reviewed plant | One plant demonstrates the migration, public wording and rollback path before any wider change. | Requires WSL-BL-013 and explicit production approval. |

Current progress: `vnext_profile.json` is defined and validated for WSL-0001
through WSL-0005. It remains passive research data until a later API decision.

## GitHub Delivery Lane

| ID | Item | Done when | Gate |
|---|---|---|---|
| WSL-BL-023 | Prepare a scoped GitHub audit/profile PR | The exact local diff is classified as research-only, checked in a clean `DennisHedegreen/windowsill-api` checkout and described in a draft PR. | Explicit commit/push/PR decision; no production files. |
| WSL-BL-024 | Record merged research evidence | Each merged audit/profile PR is linked to its workpack and LifeOS activity record with PR URL/number and merge commit. | Merge is research-only; do not infer review or promotion. |

## Recurring Operations

| ID | Item | Done when | Gate |
|---|---|---|---|
| WSL-BL-030 | Weekly health and queue readback | Live `/v1/status`, `/v1/health` and GitHub PR state are logged before any merge/release action. | Read-only. |
| WSL-BL-031 | Commit/synchronize the local Windowsill mirror intentionally | The known local docs and five research packs are reviewed as one scoped repository-health change. | Separate commit/push decision; no automatic public deployment. |
| WSL-BL-032 | Keep public counters truthful | Research-pack, reviewed-pack and production counts remain separate wherever shown. | Promotion/deploy controls remain separate. |

## Product Work — Not Pulled Forward By This Backlog

The following remain in `ROADMAP.md` and should not displace data integrity:

- coordinate-specific frost and growing-season modelling
- Danish API language support
- SDKs, downloadable dataset and companion-planting work
- Android companion app

## Not Backlog Items Without A New Decision

- bulk-creating 148 workpacks
- changing live plant count
- API deployment
- reviewer-key creation or outreach sending
- making an unreviewed pack look expert approved
