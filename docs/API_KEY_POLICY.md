# API Key Policy

Status: working policy
Updated: 2026-06-07

Windowsill API keys exist to keep the service stable, not to turn small plant tools into a paywall.

No key is required for small casual use.

Current public limits:

- no key: 60 requests / hour / IP
- free key: 1,000 requests / month
- builder key: 10,000 requests / month
- sponsored key: manual approval

## Default Answer

Small projects can ask for a free key.

This includes:

- non-commercial experiments
- school or education projects
- local community tools
- small widgets
- personal dashboards
- research prototypes
- garden, balcony or windowsill side projects
- accessibility or public-interest uses

The key question is not whether the project is polished.

The key question is whether the use is honest, small enough for the service, and not trying to hide the source or uncertainty.

## Ask By Email

Email:

```text
api@windowsill.dk
```

Include:

- who you are
- what you are building
- expected request volume
- whether the project is public
- whether it is commercial
- where Windowsill data/API output will appear
- whether you will show uncertainty/limits clearly

## Give A Free Key When

Give a free key when:

- the project is small or early
- the project is non-commercial, educational, local, experimental or public-interest
- the expected volume fits the free limit
- the user is clear about what they are building
- Windowsill is credited or at least not hidden
- the tool does not present recommendations as certainty
- the user accepts rate limits

## Reviewer Invitation / Thank-You Keys

Independent plant reviewers may receive a personal API key that works as both:

- the invitation credential for the reviewer page
- an optional free API key after the review, if they want to keep using it for small projects

This is not payment for agreement.

Reviewer keys also act as invitation links for the reviewer tool:

```text
https://windowsill.dk/review/genovese-basil/?key=PERSONAL_REVIEW_KEY
```

No cookies, account or browser-stored login is required.

Give a reviewer invitation key when:

- Dennis has approved that this person should be contacted
- the reviewer is attached to a specific plant review invitation
- the key is sent only through the outreach draft or a direct approved message
- the key is framed as access to the review tool, not as a public login
- the key can be disabled later if it is shared, abused or no longer needed

Let the same key remain as a thank-you key when:

- the reviewer has sent a real correction note or review signal
- the review is logged before the key is treated as ongoing API access
- the key is framed as optional access for small projects, teaching, prototypes or local experiments
- the key does not change the review status, score or decision

Default reviewer key:

```text
plan: free
monthly_limit: 1000
project: Windowsill reviewer access
note: Reviewer thank-you key for [plant / reviewer / date]
```

Do not issue unlimited `sponsored` keys by default. Use `sponsored` only if there is a concrete reason and the use is trusted.

Manual local helper for a reviewer invitation:

```bash
python3 windowsill/api/scripts/create_api_key.py \
  --owner "Reviewer Name" \
  --reviewer-email "reviewer@example.org" \
  --project "Windowsill reviewer access - WSL-0001 Genovese Basil" \
  --plan free \
  --review-plant WSL-0001 \
  --note "Reviewer invitation key for WSL-0001"
```

The raw key is printed once. Store and send it outside git.

Live/Railway helper for a reviewer invitation, only when `DATABASE_URL` is intentionally set:

```bash
DATABASE_URL="..." python3 windowsill/api/scripts/create_api_key.py \
  --use-database-url \
  --owner "Reviewer Name" \
  --reviewer-email "reviewer@example.org" \
  --project "Windowsill reviewer access - WSL-0001 Genovese Basil" \
  --plan free \
  --review-plant WSL-0001 \
  --note "Reviewer invitation key for WSL-0001"
```

Do not run live key creation casually.

For outreach, create only the keys Dennis has approved to send.

For thank-you access, keep the same key active only after the review has been logged.

## Say Not Yet When

Say not yet when:

- the project needs high volume but has no clear use case
- the requester wants to hide Windowsill as the source
- the requester wants plant recommendations framed as guarantee, certification or safety advice
- the use appears extractive, spammy or abusive
- the requester cannot explain the expected request volume
- the project needs reliability that Windowsill cannot honestly promise yet

## Sponsored / Builder Access

Use builder or sponsored keys only when the project needs higher limits and the use is still compatible with the project.

Sponsored does not mean paid by default.

Sponsored means manually trusted.

## Boundary

Windowsill is not a medical, toxicology, culinary-safety or horticultural certification service.

API users should keep visible limits close to the output.

Minimum public boundary:

```text
Windowsill recommendations are starting points, not guarantees. Local microclimate, shade, container, soil, watering and plant safety may differ.
```

## Funding Note

Railway still costs money.

The project is not trying to earn money from small users.

At this scale, the honest funding model may be:

```text
Pant for a plant API.
```

That is a joke, but also a policy boundary:

keep the API usable for small public projects before treating it as a product funnel.
