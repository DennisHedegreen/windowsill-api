# Windowsill Plant Research Pack Template

Copy this folder when preparing a serious plant contribution.

Suggested folder name:

```text
research-packs/WSL-XXXX-plant-name/
```

Files:

- `plant.json` — candidate plant JSON
- `source_registry.md` — sources and what each source supports
- `field_rationale.md` — why modelling values were chosen
- `uncertainty_notes.md` — weak values, disagreements and open questions
- `expert_review.md` — three independent same-plant reviewer status
- `pr_description.md` — ready-to-paste PR or email text
- `audit_state.md` — required when auditing an existing production entry; records the candidate-to-production decision state
- `vnext_profile.json` — passive future preference data; not part of the current API or scoring

This pack is required for new plants and material corrections to existing
plants. Existing seeded entries do not need to be retrofitted all at once;
audit them through the prioritized queue in [`../../BACKLOG.md`](../../BACKLOG.md).

Read [`../../docs/PLANT_DATA_STANDARD_V1.md`](../../docs/PLANT_DATA_STANDARD_V1.md)
before changing a production record.

Read [`../../docs/PLANT_PREFERENCE_PROFILE_VNEXT.md`](../../docs/PLANT_PREFERENCE_PROFILE_VNEXT.md)
before adding preference data.

Before opening a pull request, run:

```bash
python3 scripts/validate_research_packs.py
```
