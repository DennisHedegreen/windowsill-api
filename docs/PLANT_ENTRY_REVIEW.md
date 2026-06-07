# Plant Entry Review

Status: operating guide.

Use this before merging or publishing a new plant entry.

## Basic Checks

- [ ] JSON is valid.
- [ ] ID is next available `WSL-XXXX`.
- [ ] Filename matches the ID and common slug.
- [ ] Filename is listed in `plants/index.json`.
- [ ] `count` in `plants/index.json` is updated.
- [ ] Required fields are present.
- [ ] Contexts are realistic.

## Source Checks

- [ ] Accepted botanical name has a botanical authority.
- [ ] Family and genus are supported.
- [ ] Native, introduced or cultivated status is clear or marked uncertain.
- [ ] Growing conditions have a horticultural, crop or agronomy source.
- [ ] Safety concerns are checked separately from food tradition.
- [ ] Personal observation is labelled as local observation.

## Model Checks

- [ ] `min_temp` means active growth threshold, not survival.
- [ ] `hardiness_temp` means survival/overwinter tolerance.
- [ ] `hardiness_zone_min` is consistent with `hardiness_temp`.
- [ ] `sun_hours` and `sun_direct` match the plant's real behaviour.
- [ ] `windowsill`, `balcony` and `garden` contexts are not added by default.
- [ ] `habit` notes explain likely failure modes.

## Honesty Checks

- [ ] Uncertain values are named in `contributor_note`.
- [ ] AI output is not cited as evidence.
- [ ] Safety preparation is visible where relevant.
- [ ] Plant count was not prioritized over data quality.
