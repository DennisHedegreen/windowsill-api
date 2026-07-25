# Windowsill Plant Data Standard v1

Status: working standard
Updated: 2026-07-25

## Purpose

Windowsill must distinguish a useful API record from the evidence needed to
trust, correct and improve it.

The production library is not a claim that every field has received the same
level of research. It is a working baseline. The research-pack layer is the
route for making individual plant records traceable over time.

This standard makes that route explicit without pretending that all 148 seeded
entries have already been audited.

## Baseline At Adoption

- Production library: 148 plant files with one consistent query schema.
- Production source registry fields: none.
- Production expert-review fields: none.
- Valid linked research packs: 5, for WSL-0001 through WSL-0005.
- Production promotion from those packs: not done.

The five packs are evidence candidates, not proof that the corresponding live
records have already been corrected or expert reviewed.

## The Three Layers

### 1. Production record

`plants/WSL-XXXX-name.json` is the compact record used by the API.

It contains the model values needed for recommendation, such as temperature,
sun, context and habit. It stays small, stable and fast to load. A production
record is not a bibliography and must not silently imply expert approval.

The same record is mirrored in `api/plants/` while the API uses a separate
plant bundle. The two copies must match exactly after a promotion.

### 2. Plant workpack

`research-packs/WSL-XXXX-name/` is the evidence and change-proposal layer for
one plant.

Every new plant and every material correction to an existing plant must use a
workpack. The standard workpack contains:

```text
plant.json             candidate production values
source_registry.md     sources and the field claims they support
field_rationale.md     why the candidate model values were chosen
uncertainty_notes.md   weak values, limits and unresolved disagreement
expert_review.md       real review record or an honest empty state
pr_description.md      reviewable change summary
```

`plant.json` uses the production fields plus the candidate-only
`expert_review` object. It must not invent a new production schema by itself.

When a pack audits an existing production entry, add `audit_state.md`. It is a
short candidate-to-production reconciliation: what the evidence supports, what
is still a modelling or review question, and whether any production change is
proposed. It is not an expert-review substitute.

For new audit work, also add `vnext_profile.json` following
`docs/PLANT_PREFERENCE_PROFILE_VNEXT.md`. It is passive workpack data only and
must not change the present API, scoring or production record.

### 3. Decision and release record

A workpack does not promote itself. A human decision must reconcile candidate
and production values, state what changed and what remains uncertain, then
apply the normal production/deployment checks.

Until a structured public review/provenance schema is deliberately designed,
the workpack remains the source of record for review history and detailed
source rationale. Do not copy partial review claims into production `notes` as
a substitute for that decision.

## Workpack Lifecycle

```text
baseline only
  -> audit draft
  -> source-ready candidate
  -> review-ready candidate
  -> human review in progress
  -> promotion decision
  -> production update and separate deploy verification
```

Not every plant needs to pass every stage immediately. The current 148 entries
are `baseline only` unless a linked workpack says otherwise.

## Evidence Rules

- One pack covers exactly one `WSL-XXXX` plant ID.
- `source_registry.md` states what each source supports and what it does not.
- Botanical identity, cultivation/model values and safety are checked as
  separate evidence questions.
- AI can assist drafting and comparison, but is not a source.
- Estimates remain labelled as estimates, including when they are useful model
  values.
- A real reviewer may disagree. Do not convert disagreement into a false
  average or an implied expert endorsement.

## Promotion Gate

Before changing a production plant record, all of the following must be true:

1. The linked workpack passes `scripts/validate_research_packs.py`.
2. Candidate-to-production differences have been explicitly reviewed.
3. Source and uncertainty notes are adequate for the risk of the field.
4. Required human review is complete and honestly recorded. For Genovese
   Basil, that means three accepted same-plant reviews across at least two
   distinct review contexts.
5. `plants/`, `plants/index.json` and the `api/plants/` mirror are updated in
   one scoped change when applicable.
6. Deployment is separately approved, then the live API is read back before
   any public count or claim is changed.

Research-pack merge, production promotion, API deployment, reviewer-key
creation and outreach sending are separate decisions.

## What This Standard Does Not Do Yet

- It does not retrofit 148 workpacks in one batch.
- It does not add source or review fields to the production API schema.
- It does not change live plant values, counts or API versions.
- It does not create reviewer keys, send outreach or deploy anything.

The backlog in `../BACKLOG.md` orders those follow-up decisions.
