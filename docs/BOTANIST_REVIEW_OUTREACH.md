# Windowsill Botanist Review Outreach

Status: working outreach plan
Updated: 2026-06-08

Windowsill uses three independent same-plant reviewers.

Operational queue:

```text
Release Control -> Outreach
private/data/mail/contact-lists.csv -> list_windowsill_genovese_basil_reviewers
private/data/tactical/outreach-ledger.csv -> plan_20260608_windowsill_genovese_basil_three_reviewer_model
private/data/mail/drafts/windowsill/2026-06-08-windowsill-genovese-basil-review-draft.md
```

Do not mark anything as sent until the Outreach panel actually sends it or Dennis manually confirms it was sent.

The point is not to force agreement.

The point is to make disagreement visible before a research pack is promoted into the production plant library.

## First plant

Current first review candidate:

```text
research-packs/WSL-0001-genovese-basil/
```

Production promotion status:

```text
not promoted
```

## Reviewer mix

For one plant, choose three independent reviewers who can plausibly disagree because they bring different plant-knowledge contexts.

For Genovese Basil, the first target mix should be:

1. Basil horticulture / breeding
2. Basil disease / container-growing risk
3. Genovese / Italian botanical-agronomic context

This is still one same-plant review.

It is not three different scores.

## Candidate reviewers / contacts

### 1. James E. Simon — Rutgers / US Basil Consortium

Fit:

- basil breeding and horticultural innovation
- sweet basil / improved varieties
- strong match for cultivar/type, practical plant library values, and whether `Genovese` is being framed correctly

Public source:

- US Basil Consortium profile lists James E. Simon and contact email.
- Rutgers faculty profile lists him as Distinguished Professor in Plant Biology with expertise in plant diversity, natural products, plant breeding and genetic improvement.

Contact:

```text
jimsimon@rutgers.edu
```

Ask:

- Is `Ocimum basilicum 'Genovese'` acceptable as a practical Windowsill name?
- Should Windowsill store `species: basilicum` instead of `species: basil`?
- Are `grow_time_weeks: 8`, `weeks_from_transplant: 5`, and `min_temp/max_temp/optimal_temp` reasonable practical estimates?

### 2. Meg McGrath — Cornell / basil downy mildew

Fit:

- plant pathology and basil downy mildew
- strong match for disease risk, balcony/windowsill humidity, airflow, and whether `good` context ratings are too optimistic
- useful disagreement point against a simple “basil is easy” entry

Public source:

- Cornell CALS article describes McGrath's long-running work on basil downy mildew.
- Cornell vegetable monitoring pages list contact email for basil downy mildew confirmation/reporting.

Contact:

```text
mtm3@cornell.edu
```

Ask:

- Are the windowsill/balcony/garden context notes honest enough about humidity, airflow and disease risk?
- Should downy mildew be mentioned in the production `notes` for Genovese Basil?
- Is the entry too optimistic when it marks all three contexts as `good`?

### 3. Guido Lingua — Universita del Piemonte Orientale

Fit:

- general botany / plant biology
- named author on work involving `Ocimum basilicum var. Genovese`, arbuscular mycorrhizal fungi, growth and essential oil composition
- useful for botanical/agronomic interpretation of Genovese basil as plant material rather than only consumer seed-trade language

Public source:

- Universita del Piemonte Orientale profile lists Guido Lingua, contact email and botany/plant biology affiliation.
- Research record lists the Acta Horticulturae paper on `Ocimum basilicum var Genovese`.

Contact:

```text
guido.lingua@uniupo.it
```

Ask:

- Is the pack's botanical framing of Genovese Basil acceptable?
- Does `Genovese` need stronger uncertainty language as cultivar/type/production identity?
- Are the safety/aroma/essential-oil caveats proportionate for a normal culinary plant entry?

## Backup contact

### Consorzio di tutela del Basilico Genovese D.O.P

Fit:

- not an independent botanist review by itself
- useful for local/production identity, DOP naming, and whether "Genovese Basil" has regional/product meaning that Windowsill should not flatten

Contact:

```text
info@basilicogenovese.it
presidente@basilicogenovese.it
```

Use as:

- context source
- optional fourth local-practice contact
- not one of the three scientific reviewers unless a named technical reviewer responds

## Outreach email template

Subject:

```text
Short expert check request: Genovese Basil in an open plant-library API
```

Body:

```text
Hello [Name],

My name is Dennis Hedegreen. I am building Windowsill, a small public plant recommendation API and plant-library project.

https://windowsill.dk
https://github.com/DennisHedegreen/windowsill-api

The idea is simple: a person enters a location, window/balcony/garden context, direction and season, and Windowsill returns edible plants that may realistically fit that situation. It is meant as a practical, correctable tool, not as an AI gardening oracle.

I am writing because I do not want the plant library to become polished but weak data. Before a research pack is promoted into the production plant library, I want it checked by people who can disagree from real plant knowledge.

The first review candidate is Genovese Basil.

You do not need to edit JSON or use GitHub. I made a small review page that shows the entry in normal language and lets you submit a correction note directly:

https://windowsill.dk/review/genovese-basil/?key=[PERSONAL_REVIEW_KEY]

The link uses a personal reviewer API key. It does not use cookies, tracking or an account.

The underlying source pack is public here, if you want to inspect it:

https://github.com/DennisHedegreen/windowsill-api/tree/main/research-packs/WSL-0001-genovese-basil

For this first plant, I am trying a three-independent-reviewer model:

- one reviewer with basil horticulture / breeding context
- one reviewer with plant pathology / disease-risk context
- one reviewer with botanical or Genovese/Italian agronomic context

The goal is not to force agreement. The goal is to record where serious plant reviewers agree, disagree, or say that the entry is too uncertain.

I am not asking for an endorsement, a long review, or unpaid consulting. A short correction note would already be useful.

If you have time, the most useful questions are:

1. Is the botanical/name framing acceptable for a practical public plant library?
2. Is the edible/safety boundary proportionate for a normal culinary herb entry?
3. Is the windowsill/balcony/garden assessment too optimistic, too cautious, or reasonable?
4. Are the temperature and first-harvest estimates obviously wrong?
5. What should be corrected before this entry is treated as production data?

The specific fields I am trying to verify are ordinary practical fields such as `name_latin`, `species`, `context`, `habit`, `hardiness_temp`, `min_temp`, `optimal_temp`, `max_temp`, `grow_time_weeks` and `weeks_from_transplant`.

I can record your response in one of two ways:

- named expert review, if you explicitly permit that
- unnamed expert review note, if you prefer not to be named publicly

Either way, I will not present your reply as endorsement of Windowsill. I will treat it only as a correction / review signal for this plant entry.

If this is not the right route, no problem. Even a short "not my field" or "ask someone else" is useful.

As a thank-you, the same key can remain available as a free Windowsill API key for small projects, teaching, prototypes or local experiments. That is optional and does not depend on whether your review agrees with the current entry.

Thank you,

Dennis Hedegreen
api@windowsill.dk
```

## Review record template

When a reviewer answers, record only what they actually said.

Do not paraphrase into fake certainty.

```text
Reviewer:
Affiliation:
Date:
Permission to name publicly: yes / no / unclear

Botanical name:
agree / minor_fix / dispute / not_assessed

Edibility:
agree / minor_fix / dispute / not_assessed

Container fit:
agree / minor_fix / dispute / not_assessed

Climate fit:
agree / minor_fix / dispute / not_assessed

Safety:
agree / minor_fix / dispute / not_assessed

Decision:
agree / minor_fix / major_dispute / reject / not_enough_information

Notes:

Exact suggested corrections:
```

## Source notes

Sources checked for this outreach plan:

- Rutgers / US Basil Consortium profile for James E. Simon.
- Rutgers Plant Biology profile for James E. Simon.
- Cornell CALS article on Meg McGrath and basil downy mildew.
- Cornell Vegetables basil downy mildew pages listing contact route.
- Universita del Piemonte Orientale / CIB profile for Guido Lingua.
- Universita del Piemonte Orientale research page for `Ocimum basilicum var Genovese`.
- Basilico Genovese D.O.P contacts page.
