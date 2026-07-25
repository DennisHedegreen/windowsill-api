# Windowsill Plant Reviewer And Flyer Plan

Status: working plan
Updated: 2026-07-23

Windowsill needs two different public doors:

1. users who want to try the tool
2. plant people who can correct the plant library

The flyer should serve both, but the main call should stay simple:

```text
What might grow here?
windowsill.dk
```

## Flyer Target

Use the direct URL:

```text
https://windowsill.dk/
```

If a QR code is printed, the QR code should point directly to that URL.

Do not use a candidate `/q/` redirect URL until the QR Redirect Registry has a
public verified resolver.

## Flyer Audience

Primary:

- balcony growers
- windowsill growers
- community gardeners
- plant-shop staff
- seed-library people
- allotment and garden-club people
- horticulture students
- local food / edible-plant people

Secondary:

- civic tech people
- small tool builders
- teachers
- people who might want a free API key for a small project

## Flyer Message

Do not sell Windowsill as a gardening guarantee.

Say:

```text
A small public tool that reads place, direction, season and growing context,
then suggests edible plants that might fit.
```

Do not say:

```text
Grow the perfect plant.
Guaranteed recommendations.
AI knows what to plant.
```

## Reviewer Message

Plant reviewers should hear a different message:

```text
Help make the plant data less weak.
Pick one plant entry. Tell us what is wrong, too optimistic or uncertain.
```

The point is correction, not endorsement.

## First Reviewer Lane

First plant:

```text
WSL-0001 Genovese Basil
```

First review mix:

- basil horticulture / breeding
- basil disease / container-growing risk
- Genovese / Italian botanical-agronomic context

Use:

```text
windowsill/docs/BOTANIST_REVIEW_OUTREACH.md
private/data/mail/drafts/windowsill/2026-06-08-windowsill-genovese-basil-review-draft.md
```

Do not send the reviewer email until:

- Dennis has approved the recipient batch
- personal reviewer keys are created intentionally
- the key is inserted into the draft
- the send is logged

## Flyer Copy

### Front

```text
WINDOWSILL

What might grow here?

A small public tool for windowsills,
balconies and gardens.

Pick a place.
Choose a direction.
Get edible plant suggestions for this week.

windowsill.dk
```

### Back

```text
Windowsill is not a gardening oracle.

It uses climate history, direction, season and plant-library limits
to make a practical first reading.

Know plants?
Help correct one entry.

Add a plant, review Genovese Basil, or build with the API:

windowsill.dk
api@windowsill.dk
github.com/DennisHedegreen/windowsill-api
```

## Print Notes

Recommended first batch:

- A6 or A5
- matte paper
- one strong URL
- one QR code to `https://windowsill.dk/`
- no claim that the tool guarantees success
- no long explanation

If space is tight, remove GitHub first.

Keep:

- `windowsill.dk`
- `api@windowsill.dk`
- "not a gardening oracle"
