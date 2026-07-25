# Windowsill Git Flow

Status: operating guide
Updated: 2026-07-25

Windowsill uses a two-step path for new plants. The research pack comes first.
The plant library entry comes after review.

GitHub records a reviewable change; it does not make an unreviewed candidate
true, nor does a merge deploy the API.

See also:

- `docs/RESEARCH_PACK_CONTRACT.md`
- `docs/WEEKLY_MERGE_PLAN.md`
- `docs/PLANT_DATA_STANDARD_V1.md`
- `docs/PLANT_PREFERENCE_PROFILE_VNEXT.md`
- `BACKLOG.md`

## What GitHub Is Responsible For

```text
local evidence work
  -> scoped GitHub branch
  -> draft PR + automated validation
  -> human PR scope review
  -> research-only merge OR separate promotion PR
  -> separately approved deployment and live readback
```

GitHub is the public, inspectable change record. The workpack remains the
source of detailed evidence and uncertainty. A GitHub approval or merge is not
an expert plant review, a production promotion or an API release.

When working from the Hedegreen Research `windowsill/` folder, first verify
whether it is an independent checkout of `DennisHedegreen/windowsill-api`.
If it is only a local mirror, prepare the GitHub patch in a clean, separate
clone; never assume that a local change has reached GitHub.

## Branch pattern

For a new plant research pack:

```text
plant-pack/common-name
```

Example:

```text
plant-pack/garden-cress
```

For a correction:

```text
fix/plant-name-field
```

For an evidence audit of an existing entry:

```text
audit/WSL-0005-holy-basil
```

For documentation or shared contract work:

```text
docs/plant-data-standard-v1
```

Use one coherent purpose per PR. A special baseline PR may contain the shared
standard, validator support and the linked audited workpacks, but its
description must list every included plant and state that it is research-only.

## New plant flow

1. Define the PR class and scope.
2. Add one folder under `research-packs/`.
3. Use the exact research pack contract.
4. Run the validator.
5. Create a scoped branch in a clean GitHub checkout.
6. Open a draft pull request using `.github/pull_request_template.md`.
7. Confirm the `Validate research packs` check is green and inspect the changed
   paths before marking the PR ready.
8. Merge only when the pack validates and the PR is research-only.
9. Promote into `plants/` only after human review in a separate PR.

For an audit of an existing production record, include `audit_state.md`. For
audit work begun after the vNext preference contract, include
`vnext_profile.json` as well. Both files are research-only evidence files.

## PR Classes And Merge Gates

| PR class | May change | Required before merge | Merge means |
|---|---|---|---|
| Research pack | one `research-packs/WSL-.../` folder and necessary validator/docs changes | validator green, changed-path inspection, no unsupported review claim | evidence is available for future review; production is unchanged |
| Audit/profile update | existing workpack evidence files, passive profile, narrowly related documentation | validator green, candidate-to-production differences explicit, no `plants/` or `api/plants/` change | candidate is source-ready or review-ready, not promoted |
| Production promotion | one reviewed workpack plus matching `plants/`, index and API mirror changes | completed human-review gate, explicit decision record, mirror check | production repository changes; deployment remains separate |
| API/service change | runtime, auth, deployment or API contract files | focused tests and release-risk review | code is merged; deployment and live readback remain separate |

Before merging any PR, classify every changed path. Stop if a PR marked
research-only touches `plants/`, `plants/index.json`, `api/plants/`, runtime,
deployment or credential/configuration files.

Creating a branch, committing, pushing and opening a PR are intentional GitHub
actions. Do those only when the requested change set and its PR class are clear.

## What can merge early

A correct research pack may merge before the plant becomes part of the API library.

That means:

- `research-packs/WSL-XXXX-plant-name/` may merge as a pending contribution
- `plants/WSL-XXXX-plant-name.json` should wait until review
- `plants/index.json` should wait until the plant is accepted
- public plant count should not change when only a research pack merges

This keeps the public contribution pipeline open without silently trusting AI output.

## After main merge

After a research-pack PR merges into `main`:

- update research-pack status/count if shown publicly
- do not update live API plant count
- do not deploy the API unless production plant files changed
- keep the pack marked pending review
- record the PR URL/number and merge commit in the relevant operational log

After a production plant promotion merges into `main`:

- update `plants/index.json`
- update API bundle plant files if separate
- update README/reference/public website count claims
- deploy API and verify live status
- update release notes / operational memory

## Pull request expectations

Every plant-pack PR should say:

- plant name
- region context
- whether ChatGPT or another AI tool helped
- sources used
- uncertainty
- whether expert review exists
- whether this is only a research pack or a proposed plant-library promotion

Every audit/profile PR should additionally say:

- production ID and current production state
- whether `audit_state.md` and `vnext_profile.json` are included
- exact fields that remain estimates or human-review questions
- explicit confirmation that no API/scoring, location-light, 3D/shade or
  watering calculation is introduced

## Merge rule

Do not merge a plant-pack PR if:

- required files are missing
- `plant.json` is invalid
- sources are empty
- uncertainty is missing
- AI output is presented as source truth
- expert review is claimed without notes
- the PR tries to add many unrelated plants at once

## Reviewers

Windowsill may later use three independent reviewers per plant.

That does not mean three different roles.

It means three independent plant-knowledge reviewers looking at the same plant, because plant knowledge often contains disagreement.
