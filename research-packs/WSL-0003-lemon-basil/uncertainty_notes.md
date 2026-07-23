# Uncertainty notes — WSL-0003 Lemon Basil

## High-level uncertainty

Lemon Basil is a normal culinary herb, but this entry has higher naming uncertainty than Genovese Basil and Thai Basil.

The main issue is botanical identity: the production file uses `Ocimum × citriodorum`, while several lemon-basil-specific secondary sources use `Ocimum × africanum` and treat `Ocimum × citriodorum` as a synonym. This needs human/expert review before any production correction.

## Estimated values

The following values are estimates:

- `name_latin: "Ocimum × africanum"`
  - Candidate correction from existing `Ocimum × citriodorum`.
  - Needs botanical review before production promotion or correction.

- `species: "africanum"`
  - Used as the epithet part of the candidate hybrid name.
  - The current schema has no separate hybrid-marker field.

- `min_temp: 15`
  - Used as practical lower active-growth threshold.
  - Not a survival threshold.
  - Basil may survive cooler short exposures, but cold reduces performance.

- `max_temp: 33`
  - Used as practical upper recommendation threshold before heat/water/quality stress becomes likely.
  - Not a death temperature.

- `optimal_temp: 26`
  - Model value inside the general basil optimal range supported by Rutgers.
  - Existing `22` is probably too cool as the main sweet spot for a warm-season basil.

- `sun_hours: 6`
  - Existing `5` is probably too low for a robust full-sun basil recommendation.
  - Indoor and outdoor sun are not equivalent.

- `grow_time_weeks: 7`
  - Practical estimate for first realistic edible harvest from seed/sowing.
  - Existing `6` may be possible for small early pinching but is optimistic for a useful culinary harvest.

- `weeks_from_transplant: 4`
  - Practical estimate for first realistic edible harvest after transplanting or buying a young plant.
  - Existing `3` may be possible for small early picking but is optimistic.

- `hardiness_temp: 0`
  - Used only as frost boundary / survival-risk simplification.
  - Basil is frost-sensitive and should not be recommended for freezing conditions.

- `hardiness_zone_min: 10`
  - Approximate horticultural modelling value.
  - Lemon basil should be treated as annual in temperate climates.

## Source disagreements

- Existing Windowsill production entry uses `Ocimum × citriodorum`.
- Lemon-basil-specific secondary sources commonly use `Ocimum × africanum`.
- Some gardening sources use labels such as `Ocimum basilicum citriodorum`.
- Some sources confuse or blur Lemon Basil with `Mrs. Burns' Lemon`, which is a different lemon-scented basil cultivar/type.
- General basil sources support the growing model but are not Lemon-Basil-specific.
- Harvest timing sources vary between first leaves, early pinching, maturity and repeated harvest.

## Naming uncertainty

- Candidate name in this pack: `Ocimum × africanum`.
- Existing production name: `Ocimum × citriodorum`.
- Possible interpretation: `Ocimum × citriodorum` is a synonym or horticultural/trade label.
- Expert review should decide whether Windowsill should:
  - keep `Ocimum × citriodorum`,
  - change to `Ocimum × africanum`, or
  - use a more conservative label while noting the synonym issue.
- The current schema has no separate field for `synonyms`, `hybrid_parentage` or `cultivar_group`, and this pack intentionally does not add new fields.

## Safety uncertainty

Low uncertainty for normal culinary use:

- Leaves are commonly used as food.
- Tender stems may be used with leaves in normal culinary contexts.

Boundary uncertainty:

- This entry does not assess essential oil.
- This entry does not assess supplements.
- This entry does not assess extracts.
- This entry does not assess medicinal dosing.
- This entry does not assess pregnancy-specific safety.
- This entry does not assess allergy risk.
- This entry does not assess seed-gel use.
- BfR alkenylbenzene concerns apply as a caution around higher-exposure herb/spice/extract/supplement contexts, not as proof that ordinary Lemon Basil leaves are unsafe.

## Context uncertainty

### Windowsill

Included, but conditional:

- Needs strong light.
- Needs warmth.
- Needs drainage.
- Needs airflow.
- Indoor winter light may be insufficient in northern regions.
- Cold glass and drafts may stunt growth.

### Balcony

Included, but seasonal:

- Works best in warm, sunny, frost-free conditions.
- Small pots dry quickly.
- Wind and cold nights can damage plants.
- Hot balconies may need extra water or some afternoon shade.

### Garden

Included, but frost-free:

- Suitable during warm season.
- Not suitable for frost/cold periods.
- Wet, crowded planting raises disease risk.
- Treat as annual in temperate climates.

## Existing production fields that need human review

Existing entry reviewed from `plants/WSL-0003-lemon-basil.json`:

- `name_latin: "Ocimum × citriodorum"`
  - Suggested review: consider `Ocimum × africanum` as candidate accepted name.

- `species: "basil"`
  - Suggested correction: `africanum` if using `Ocimum × africanum`, or another agreed hybrid convention.

- `optimal_temp: 22`
  - Suggested correction: `26` as practical warm-season sweet spot.

- `sun_hours: 5`
  - Suggested correction: `6`.

- `grow_time_weeks: 6`
  - Suggested correction: `7` as first realistic edible harvest estimate.

- `weeks_from_transplant: 3`
  - Suggested correction: `4`.

- `hardiness_temp: -1`
  - Suggested correction: `0`, with clear note that basil is frost-sensitive.

## Review recommendation

Mark this pack as:

`needs_human_check`

Do not mark as expert reviewed until three independent reviewers have actually assessed botanical name, edibility, container fit, climate fit and safety.
