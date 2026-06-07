# Windowsill Weekly Merge Plan

Status: operating guide
Updated: 2026-06-08

Windowsill should not update public counts casually after every merge.

There are two different merge types:

1. Research-pack merge
2. Production plant promotion

Only the second one changes the live plant count.

## Public counters

Track these separately:

| Counter | Meaning | Changes when |
|---|---|---|
| Production plants | Accepted plant JSON files in `plants/` and live API library | A reviewed plant is promoted into `plants/` and deployed |
| Research packs | Candidate/audit packs in `research-packs/` | A valid research pack PR merges |
| Expert-reviewed packs | Research packs with three real independent reviews | Three reviewer notes are present and the summary is updated |
| Pending review | Research packs that are not promoted yet | A pack exists but has not passed review/promotion |

Do not describe a research-pack merge as a new live plant.

## Weekly rhythm

Use one weekly Windowsill merge/release window unless there is an urgent fix.

Recommended default:

```text
Sunday or Monday:
  review pending packs
  merge valid research packs
  decide if any pack is ready for promotion
  update public counters
  deploy only if production plants changed
```

## Research-pack merge checklist

Before merging a research pack:

- GitHub Action `Validate research packs` is green.
- Local validator passes if checked manually.
- Pack has exactly one plant folder.
- Required files are present.
- `plant.json` does not add schema fields.
- `expert_review.status` is honest.
- Text does not claim production acceptance.
- PR body says whether this is research-pack only.

After merging a research pack:

- GitHub main contains the pack under `research-packs/`.
- Do not change `plants/index.json`.
- Do not change live API plant count.
- Update public copy only if it displays research-pack count or pending-review status.
- Log the merge in the project/workpack state.

## Production promotion checklist

Before promoting a plant into `plants/`:

- Research pack exists.
- Human review is complete enough for the risk level.
- Expert review is complete if required.
- Source and uncertainty notes are acceptable.
- Candidate values are reconciled with the current schema.
- `plants/WSL-XXXX-name.json` is updated or added.
- `plants/index.json` count and file list are updated.
- `api/plants/` copy is updated if the API bundle still uses a separate copy.
- README/reference/library count claims are updated.
- API version or library version is updated if the release policy requires it.

After promotion:

- Run plant/API validation.
- Deploy the API.
- Verify live `/v1/status`, `/v1/health`, `/v1/library` and the promoted plant endpoint.
- Update `windowsill.dk` and any Hedegreen Research public claims that show the count.
- Log the deployment.

## Current state

As of 2026-06-08:

- Production plant count: 148
- Merged research packs: 1
- First merged research pack: `research-packs/WSL-0001-genovese-basil/`
- Production promotion from that pack: not done

## Default next step

Do not add new schema fields.

Next useful system work:

- build reviewer/public-signal tools
- review `WSL-0001 Genovese Basil`
- decide whether and how reviewed packs become production plant updates
