# Collaborator Setup

Short working guide for inviting people into `windowsill-api`.

## Default Collaboration Mode

Use pull requests against `main`.

Preferred default:

- outside contributors: fork + pull request
- trusted repeat contributors: write access is fine, but still use pull requests

Do not treat direct pushes to `main` as the normal path.

## Before You Invite People

Check these first:

- `README.md` reflects the current public domain and API status
- `api/.env.example` reflects the current deployment domain
- local-only files stay local: `.env`, `api/.venv/`, `api/keys.db`
- `python3 scripts/validate_research_packs.py` still passes

## Suggested GitHub Settings

- branch protection on `main`
- require pull request before merge
- require status checks:
  - `Validate research packs`
- disallow force pushes to `main`

If only research packs are changing, contributors do not need deployment access.

## What To Tell Contributors

Start here:

1. `README.md`
2. `CONTRIBUTING.md`
3. `docs/GITFLOW.md`
4. `docs/RESEARCH_PACK_CONTRACT.md`

For AI-assisted plant additions, point them to:

- `docs/CHATGPT_PLANT_RESEARCH_GUIDE.md`
- `docs/AI_PLANT_WORKFLOW.md`

## Maintainer Rule

Merge research packs only when:

- the pack validates
- the source/uncertainty files are present
- AI is not treated as the source
- the PR scope is narrow enough to review honestly

Promote into `plants/` only after review.
