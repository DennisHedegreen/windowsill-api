# Community Signal

Status: design direction, not implemented in the API.

Community signal is separate from taxonomic review.

Taxonomic review answers:

> Do taxonomy-oriented reviewers agree with the plant entry?

Community signal answers:

> Have people actually grown, known, named, eaten, failed with or observed this plant in real contexts?

Both are useful. They must not be merged into one score.

## Community Signal Can Capture

- local names
- growing reports
- climate context
- photos
- failures
- harvest success
- edible part used
- preparation notes
- regional knowledge
- user confidence

## Community Quiz

Use `docs/templates/community-grow-report.md`.

## Example Public Badge

```text
Taxonomic review: 2/3
Community signal: strong
Field reports: 84
Disputed fields: latin_name, cultivar_status
```

## Disagreement Rule

If community reports conflict with taxonomic review, show the conflict.

Example:

```text
Community reports show this plant is widely grown under this local name, but taxonomy reviewers disagree about whether the entry should be species-level or cultivar-level.
```

The point is not false certainty.

The point is to make plant knowledge more readable.
