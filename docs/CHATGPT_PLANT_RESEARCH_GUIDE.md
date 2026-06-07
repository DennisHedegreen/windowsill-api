# Add a plant with ChatGPT

Status: public guide
Updated: 2026-06-07

You do not need to be a developer to suggest a plant for Windowsill.

If you know a plant that should be in the library, the useful first step is not perfect JSON.

The useful first step is a small research pack:

```text
plant.json
source_registry.md
field_rationale.md
uncertainty_notes.md
pr_description.md
```

ChatGPT can help prepare that pack.

It must not be treated as the source of truth.

## The simple flow

1. Pick one plant.
2. Copy the prompt below into ChatGPT.
3. Replace the bracketed fields.
4. Read the answer.
5. Check the sources.
6. Correct anything you know is wrong.
7. Send the pack by GitHub pull request, GitHub issue, or email.

Email:

```text
api@windowsill.dk
```

## Copy-paste prompt

```text
You are helping me prepare one plant contribution for the Windowsill API plant library.

Windowsill is a geo-climate edible plant recommendation API. It recommends plants for windowsill, balcony and garden contexts using location, orientation, season, plant habit, temperature, sun and uncertainty.

Important rules:
- Do not invent facts.
- Do not treat ChatGPT as the source.
- Use sources and say what each source supports.
- Mark weak or uncertain values clearly.
- Do not casually say a plant is edible if preparation, dosage, plant part or safety matters.
- Only include contexts where the plant can realistically work: windowsill, balcony, garden.
- If the plant is risky, invasive, toxic, medicinal, phototoxic or only conditionally edible, say so clearly.

Plant I want to add:
[COMMON NAME]

Local name or language, if relevant:
[LOCAL NAME]

Country or region context:
[COUNTRY / REGION]

Known Latin name, if I know it:
[LATIN NAME OR "unknown"]

My personal observation, if any:
[HAVE YOU GROWN IT? WHERE? WHAT HAPPENED?]

Task:
Prepare a Windowsill research pack with these five sections.

1. plant.json
- Draft a candidate Windowsill plant JSON.
- Use WSL-XXXX as placeholder ID unless I provide the next ID.
- Include contributor_note with source and uncertainty summary.
- Include realistic values for:
  - min_temp
  - max_temp
  - optimal_temp
  - sun_hours
  - sun_direct
  - context
  - grow_time_weeks
  - weeks_from_transplant
  - hardiness_temp
  - hardiness_zone_min
  - habit
  - notes

2. source_registry.md
- List sources used.
- For each source, say exactly what it supports.
- Prefer botanical and horticultural sources over blogs.
- Separate personal observation from published sources.

3. field_rationale.md
- Explain why each modelling value was chosen.
- Explain whether the plant fits:
  - windowsill
  - balcony
  - garden
- If a context is excluded, explain why.

4. uncertainty_notes.md
- List values that are estimates.
- List source disagreements.
- List safety, naming or regional uncertainty.

5. pr_description.md
- Write a short pull-request or email description.
- Include sources.
- Include uncertainty.
- Include what still needs human review.

Before finalising:
- Check whether the accepted botanical name may differ from the common name.
- Check food safety and edible part carefully.
- Check whether the plant realistically fits a small container.
- If you are unsure, say "uncertain" instead of guessing.
```

## What to send

If you are not using GitHub, send this by email:

```text
Subject: Windowsill plant suggestion — [plant name]

Plant:
Region:
Why it matters:
Have you grown it:
Sources:
Uncertainty:

Attach or paste:
- plant.json
- source_registry.md
- field_rationale.md
- uncertainty_notes.md
- pr_description.md
```

## What Windowsill needs most

Good contributions are not just more plants.

Good contributions make plant knowledge more traceable.

Especially useful:

- local edible plants missing from the library
- balcony or windowsill growing reports
- corrections to weak entries
- safety caveats
- local names
- better source links
- evidence that a plant does not fit a context

## What not to do

Do not send:

- a plant list with no sources
- AI-generated facts with no checking
- medicinal claims without caution
- unsafe edible claims
- every context selected by default
- invented hardiness or temperature values

## A good uncertainty note is welcome

It is fine to write:

```text
I found three sources for the accepted name, but only one source for container behaviour. The windowsill context is uncertain, so I marked it risky instead of good.
```

That is useful.

False confidence is not useful.

## Why this matters

Windowsill should become an open, AI-assisted, human-accountable plant knowledge system.

AI can help with the boring structure.

Humans still have to carry the responsibility.
