# Uncertainty Notes

Uncertainty is part of Windowsill's data model.

A useful uncertain entry is better than a confident false entry.

## Where To Put Uncertainty

Use `contributor_note` for short uncertainty visible in API output.

Use contribution work pack files for longer uncertainty:

- `source_registry.md`
- `field_rationale.md`
- `uncertainty_notes.md`
- `pr_description.md`

## Good Uncertainty Notes

Good notes say what is weak and why.

Examples:

```text
hardiness_temp is estimated from RHS hardiness guidance, not a direct crop trial.
```

```text
max_temp is based on related pepper-family extension guidance, not this cultivar specifically.
```

```text
Native range is uncertain because taxonomy sources and culinary usage describe the plant differently.
```

## Bad Uncertainty Notes

Avoid vague notes:

```text
AI says this should work.
```

```text
Probably fine.
```

```text
Needs checking.
```

If something needs checking, say what needs checking.

## Field-Level Rule

If a value is estimated, say so.

If sources disagree, say so.

If personal observation is local, say where and in what context.

If a safety claim is uncertain, do not recommend consumption.
