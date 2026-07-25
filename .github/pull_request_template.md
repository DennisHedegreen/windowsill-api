## What this PR does

-

## Type

- [ ] Research pack only
- [ ] Plant library promotion
- [ ] Correction
- [ ] Documentation

## If this adds a research pack

- Folder:
- Plant:
- Region context:
- AI assisted: yes / no
- Sources listed in `source_registry.md`: yes / no
- Uncertainty listed in `uncertainty_notes.md`: yes / no
- Expert review status: not_reviewed / in_review / reviewed

## If this audits an existing plant or adds a passive preference profile

- Production ID:
- `audit_state.md` included: yes / no / not applicable
- `vnext_profile.json` included: yes / no / not applicable
- Production fields changed: yes / no
- API/scoring, location-light, 3D/shade or watering calculation changed: yes / no
- Remaining estimates or review questions:

## Review notes

- [ ] `python3 scripts/validate_research_packs.py` passes
- [ ] AI is not treated as a source
- [ ] Food safety caveats are visible
- [ ] Context fit is not overstated
- [ ] Research-only PR does not touch `plants/`, `plants/index.json` or `api/plants/`
- [ ] Production-promotion PR has a separate human-review decision record
