# Taxonomic Review

Status: design direction, not implemented in the API.

Windowsill should eventually include a taxonomic review layer.

Do not call this official academic approval.

Better terms:

- Taxonomic Review Score
- Botanical Review Score
- Expert Taxonomy Agreement

## Purpose

Taxonomic review answers:

> Do taxonomy-oriented reviewers agree with this plant entry?

It does not answer:

- whether the plant grows well in every location
- whether every culinary use is safe
- whether community reports are correct
- whether the entry is permanently true

## Proposed Score

- `0/3`: not taxonomically reviewed
- `1/3`: one independent taxonomy-oriented reviewer agrees
- `2/3`: two independent taxonomy-oriented reviewers agree
- `3/3`: three independent taxonomy-oriented reviewers agree
- `disputed`: reviewers materially disagree

Important:

`3/3` does not mean eternal truth. It means three independent taxonomy-oriented reviewers agree with the current entry, given the cited sources.

## Reviewer Quiz

Use `docs/templates/taxonomy-review-quiz.md`.

Reviewers should check:

- accepted Latin name
- family
- genus
- species / cultivar / variety treatment
- missing synonyms
- misleading common names
- native, introduced or cultivated status
- whether the entry should be split or merged
- best source for the entry
- verdict
- confidence

## Public Display Rule

Show disagreement.

Do not collapse disagreement into a fake approval badge.
