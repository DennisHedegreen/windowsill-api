# Windowsill Git Flow

Status: operating guide
Updated: 2026-06-07

Windowsill uses a two-step path for new plants.

The research pack comes first.

The plant library entry comes after review.

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

For documentation:

```text
docs/topic-name
```

## New plant flow

1. Create a branch.
2. Add one folder under `research-packs/`.
3. Use the exact research pack contract.
4. Run the validator.
5. Open a pull request.
6. Merge only when the pack validates.
7. Promote into `plants/` only after human review.

## What can merge early

A correct research pack may merge before the plant becomes part of the API library.

That means:

- `research-packs/WSL-XXXX-plant-name/` may merge as a pending contribution
- `plants/WSL-XXXX-plant-name.json` should wait until review
- `plants/index.json` should wait until the plant is accepted

This keeps the public contribution pipeline open without silently trusting AI output.

## Pull request expectations

Every plant-pack PR should say:

- plant name
- region context
- whether ChatGPT or another AI tool helped
- sources used
- uncertainty
- whether expert review exists
- whether this is only a research pack or a proposed plant-library promotion

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
