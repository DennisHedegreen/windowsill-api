# Windowsill Weekly Operating Guide

Status: practical operator guide
Updated: 2026-07-23

This is the weekly rhythm for keeping Windowsill alive without turning every
small change into a production release.

The rule is simple:

```text
research packs can merge weekly
production plant data changes only after review
public counts only change when the relevant counter actually changes
```

## Current Operating Shape

Windowsill has three public surfaces:

- API: `https://api.windowsill.dk`
- Public site: `https://windowsill.dk`
- Hedegreen Research TID tool: `https://hedegreenresearch.com/tid/windowsill/tool/`

The live API is hosted on Railway in the `reliable-curiosity` project:

- service: `windowsill-api`
- database: `Postgres`
- custom domain: `api.windowsill.dk`

The public GitHub source is:

```text
DennisHedegreen/windowsill-api
```

The local working mirror in this repository is:

```text
windowsill/
```

## Weekly Slot

Use one weekly Windowsill slot, preferably Sunday or Monday.

Default timebox:

```text
45-90 minutes
```

Do not use the weekly slot for open-ended feature work. Use it for keeping the
system clean, reviewed and moving.

## Weekly Checklist

### 1. Read Live State

Check the live API first:

```bash
curl -sS https://api.windowsill.dk/v1/status
curl -sS https://api.windowsill.dk/v1/health
```

Expected stable shape:

```text
status: ok
api_version: 0.6.0
library_version: 2026-06-07
scoring_version: 0.8.0
plant_count: 148
```

If the live API is down, stop the weekly merge lane and handle service recovery
first.

### 2. Read GitHub Queue

Check open PRs:

```bash
gh pr list --repo DennisHedegreen/windowsill-api
```

For each PR, classify it as one of these:

| Type | Meaning | Default action |
|---|---|---|
| Research pack | Adds one folder under `research-packs/` | Review and merge if clean |
| Production promotion | Changes `plants/`, `plants/index.json` or API plant bundle | Requires review gate |
| API/service fix | Changes API runtime, deployment or auth | Treat as release-risk work |
| Stale/generated fix | Old automated PR or superseded branch | Close if no longer needed |

Current first cleanup target:

```text
PR #1 Railway deploy fix is stale/dirty and should be closed if main already contains the working path fix.
```

### 3. Validate Research Packs

From the local HR repository:

```bash
python3 windowsill/scripts/validate_research_packs.py
```

For GitHub PRs, also confirm:

- `Validate research packs` is green.
- The PR normally adds exactly one research-pack folder. A shared baseline
  audit/profile PR must explicitly list every included workpack and why it is
  one coherent research-only change.
- An audit of an existing entry includes `audit_state.md`; work begun after the
  preference contract also includes passive `vnext_profile.json`.
- It does not change `plants/`.
- It does not change `plants/index.json`.
- It does not change `api/plants/`, scoring, runtime, deployment or credentials.
- It does not claim production acceptance.
- `expert_review.md` does not claim expert review unless real review happened.

### 4. Merge Research Packs

Research-pack PRs may be merged when clean.

After merge:

- Do not deploy the API just because a research pack merged.
- Do not change the production plant count.
- Update research-pack counters if a public surface shows them.
- Log the merge in the relevant project state.
- Record the PR number/URL and merge commit with the workpack or activity log.

Suggested merge wording:

```text
Merged as research pack only. No production plant promotion. No live plant-count change.
```

### 5. Production Promotion Gate

Do not promote a plant into production unless the review gate is satisfied.

For the first plant, `WSL-0001 Genovese Basil`, the gate is:

```text
minimum accepted same-plant reviews: 3
minimum distinct review contexts: 2
preferred distinct review contexts: 3
```

The reviews do not need to agree.

The production decision must record:

- what changed
- what reviewers agreed on
- what reviewers disagreed about
- where Windowsill chose cautious wording
- what remains uncertain

Only then update:

- `plants/WSL-XXXX-name.json`
- `plants/index.json`
- `api/plants/`
- README/reference/library count claims if needed
- API/library version if release policy requires it

### 6. Deploy Only When Needed

Deploy the API only for:

- production plant changes
- API/runtime changes
- auth/reviewer-flow changes
- urgent service fixes

After deployment, verify:

```bash
curl -sS https://api.windowsill.dk/v1/status
curl -sS https://api.windowsill.dk/v1/health
curl -sS "https://api.windowsill.dk/v1/recommend?lat=55.6761&lng=12.5683&orientation=S&context=windowsill&limit=3&format=compact"
```

Do not claim live state from local files alone.

## Weekly Outreach Lane

The weekly merge slot may include one small outreach action.

Do not make outreach depend on perfect automation.

Allowed weekly outreach actions:

- identify 3-5 relevant plant reviewers
- prepare one clean email draft
- create approved reviewer keys
- send one small batch
- log replies

Not allowed as a casual weekly action:

- mass-mailing people
- issuing unlimited API keys
- treating non-reply as rejection
- promoting plant data because nobody objected

## First Four Weeks Back

### Week 1: Clean The GitHub Queue

- Close stale PR #1 if confirmed obsolete.
- Review PRs #16, #17, #18 and #22 as research-pack-only PRs.
- Merge the clean research packs.
- Update research-pack count where public copy shows it.

### Week 2: Genovese Reviewer Setup

- Re-check `docs/BOTANIST_REVIEW_OUTREACH.md`.
- Choose the first 3-5 recipients.
- Create only the reviewer keys that will actually be sent.
- Send the first batch or stage it for Dennis to send.

### Week 3: Public Contribution Surface

- Check `windowsill.dk/contribute.html` and the GitHub contribution docs.
- Make sure the research-pack prompt still matches the six-file contract.
- Add a simple "review a plant" path if the flyer sends plant people to the site.

### Week 4: Review Reply Handling

- Log any replies.
- Convert each useful reply into a review record.
- Do not average reviews into a score.
- Decide whether more reviewers are needed before production promotion.

## Stop Rules

Stop and ask before doing any of these:

- deploying API changes
- creating live reviewer keys
- sending outreach
- changing production plant count
- changing DNS, Railway service config or database config
- uploading a new `windowsill.dk` public site version

## Default Next Action

The GitHub queue is currently clean and the five basil packs are already merged
as research-only candidates. The next useful action is to prepare one scoped
audit/profile documentation PR from the local workbench, then open it only when
the exact diff is intentionally approved. That PR must not change production.
