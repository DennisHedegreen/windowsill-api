#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PACK_ROOT = ROOT / "research-packs"

REQUIRED_FILES = [
    "plant.json",
    "source_registry.md",
    "field_rationale.md",
    "uncertainty_notes.md",
    "expert_review.md",
    "pr_description.md",
]

REQUIRED_PLANT_FIELDS = [
    "id",
    "contributor",
    "contributor_note",
    "name_en",
    "name_latin",
    "family",
    "genus",
    "species",
    "type",
    "min_temp",
    "max_temp",
    "optimal_temp",
    "sun_hours",
    "sun_direct",
    "context",
    "grow_time_weeks",
    "weeks_from_transplant",
    "hardiness_temp",
    "hardiness_zone_min",
    "habit",
    "notes",
    "expert_review",
]

NUMERIC_FIELDS = [
    "min_temp",
    "max_temp",
    "optimal_temp",
    "sun_hours",
    "grow_time_weeks",
    "weeks_from_transplant",
    "hardiness_temp",
    "hardiness_zone_min",
]

VALID_CONTEXTS = {"windowsill", "balcony", "garden"}
VALID_SUN_DIRECT = {"full", "partial", "shade"}
VALID_HABIT_VALUES = {"good", "acceptable", "risky", "unsuitable", "unknown"}
VALID_EXPERT_STATUSES = {"not_reviewed", "in_review", "reviewed"}
VALID_EXPERT_DECISIONS = {
    "pending",
    "accepted",
    "accepted_with_caution",
    "needs_more_sources",
    "rejected",
}

PROFILE_STATUSES = {"draft", "source_ready", "reviewed"}
DIRECT_SUN_PREFERENCES = {"full_sun", "part_sun", "shade", "unknown"}
LIGHT_TOLERANCES = {"good", "conditional", "not_suitable", "unknown"}
SUPPLEMENTAL_LIGHT_VALUES = {"may_help", "not_needed", "unknown"}
CONTAINER_VALUES = {"yes", "conditional", "no", "unknown"}
MOISTURE_VALUES = {"evenly_moist", "allow_partial_dry", "dry_between_waterings", "unknown"}
TOLERANCE_VALUES = {"low", "medium", "high", "unknown"}
ESTABLISHMENT_VALUES = {
    "indoor_start": {"recommended", "optional", "not_recommended", "unknown"},
    "direct_sow": {"after_frost", "season_dependent", "not_recommended", "unknown"},
    "transplant": {"suitable", "conditional", "not_recommended", "unknown"},
}


def fail(errors: list[str], path: Path, message: str) -> None:
    errors.append(f"{path.relative_to(ROOT)}: {message}")


def non_empty_markdown(path: Path, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8", errors="replace").strip()
    if len(text) < 40:
        fail(errors, path, "file is too short to be useful")
    if "ChatGPT" in text and "source" not in text.lower() and "uncertain" not in text.lower():
        fail(errors, path, "mentions ChatGPT without source or uncertainty context")


def validate_expert_review(pack: Path, data: dict, errors: list[str]) -> None:
    path = pack / "plant.json"
    review = data.get("expert_review")
    if not isinstance(review, dict):
        fail(errors, path, "`expert_review` must be an object")
        return
    if review.get("model") != "three_independent_reviewers_per_plant":
        fail(errors, path, "`expert_review.model` must be three_independent_reviewers_per_plant")
    if review.get("reviewers_required") != 3:
        fail(errors, path, "`expert_review.reviewers_required` must be 3")
    if review.get("status") not in VALID_EXPERT_STATUSES:
        fail(errors, path, "`expert_review.status` has invalid value")
    if review.get("decision") not in VALID_EXPERT_DECISIONS:
        fail(errors, path, "`expert_review.decision` has invalid value")
    if not isinstance(review.get("reviews"), list):
        fail(errors, path, "`expert_review.reviews` must be a list")
    summary = review.get("agreement_summary")
    if not isinstance(summary, dict):
        fail(errors, path, "`expert_review.agreement_summary` must be an object")
    else:
        for key in ["botanical_name", "edibility", "container_fit", "climate_fit", "safety"]:
            if key not in summary:
                fail(errors, path, f"`expert_review.agreement_summary.{key}` is missing")
    if review.get("status") == "reviewed" and len(review.get("reviews", [])) < 3:
        fail(errors, path, "`expert_review.status` cannot be reviewed with fewer than 3 reviews")
    if review.get("status") == "not_reviewed" and review.get("reviews"):
        fail(errors, path, "`expert_review.status` is not_reviewed but reviews are present")


def validate_plant_json(pack: Path, errors: list[str]) -> None:
    path = pack / "plant.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(errors, path, f"invalid JSON: {exc}")
        return

    if not isinstance(data, dict):
        fail(errors, path, "root must be an object")
        return

    for field in REQUIRED_PLANT_FIELDS:
        if field not in data:
            fail(errors, path, f"missing required field `{field}`")

    for field in ["id", "contributor", "contributor_note", "name_en", "name_latin", "notes"]:
        if field in data and not str(data[field]).strip():
            fail(errors, path, f"`{field}` must not be empty")

    for field in NUMERIC_FIELDS:
        if field in data and not isinstance(data[field], (int, float)):
            fail(errors, path, f"`{field}` must be numeric")

    if data.get("sun_direct") not in VALID_SUN_DIRECT:
        fail(errors, path, "`sun_direct` must be full, partial, or shade")

    contexts = data.get("context")
    if not isinstance(contexts, list) or not contexts:
        fail(errors, path, "`context` must be a non-empty list")
    elif any(context not in VALID_CONTEXTS for context in contexts):
        fail(errors, path, "`context` contains an invalid value")

    habit = data.get("habit")
    if not isinstance(habit, dict):
        fail(errors, path, "`habit` must be an object")
    else:
        for key in ["windowsill", "balcony", "garden", "note"]:
            if key not in habit:
                fail(errors, path, f"`habit.{key}` is missing")
        for key in ["windowsill", "balcony", "garden"]:
            if habit.get(key) not in VALID_HABIT_VALUES:
                fail(errors, path, f"`habit.{key}` has invalid value")
        if not str(habit.get("note", "")).strip():
            fail(errors, path, "`habit.note` must not be empty")

    validate_expert_review(pack, data, errors)


def validate_vnext_profile(pack: Path, plant_data: dict, errors: list[str]) -> None:
    path = pack / "vnext_profile.json"
    if not path.exists():
        return
    try:
        profile = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(errors, path, f"invalid JSON: {exc}")
        return
    if not isinstance(profile, dict):
        fail(errors, path, "root must be an object")
        return
    if profile.get("schema_version") != "windowsill.plant-preferences.v0":
        fail(errors, path, "`schema_version` must be windowsill.plant-preferences.v0")
    if profile.get("api_use") != "not_active":
        fail(errors, path, "`api_use` must be not_active until a future API contract")
    if profile.get("plant_id") != plant_data.get("id"):
        fail(errors, path, "`plant_id` must match `plant.json.id`")
    if profile.get("status") not in PROFILE_STATUSES:
        fail(errors, path, "`status` has an invalid value")

    light = profile.get("light")
    if not isinstance(light, dict):
        fail(errors, path, "`light` must be an object")
    else:
        if light.get("direct_sun_preference") not in DIRECT_SUN_PREFERENCES:
            fail(errors, path, "`light.direct_sun_preference` has an invalid value")
        for key in ["bright_indirect_tolerance", "low_light_tolerance"]:
            if light.get(key) not in LIGHT_TOLERANCES:
                fail(errors, path, f"`light.{key}` has an invalid value")
        if light.get("supplemental_light") not in SUPPLEMENTAL_LIGHT_VALUES:
            fail(errors, path, "`light.supplemental_light` has an invalid value")
        hours = light.get("minimum_direct_sun_hours")
        if hours is not None and (not isinstance(hours, (int, float)) or hours < 0 or hours > 24):
            fail(errors, path, "`light.minimum_direct_sun_hours` must be null or 0–24")

    container = profile.get("container")
    if not isinstance(container, dict):
        fail(errors, path, "`container` must be an object")
    elif container.get("container_suitable") not in CONTAINER_VALUES:
        fail(errors, path, "`container.container_suitable` has an invalid value")

    water = profile.get("water")
    if not isinstance(water, dict):
        fail(errors, path, "`water` must be an object")
    else:
        if water.get("moisture_preference") not in MOISTURE_VALUES:
            fail(errors, path, "`water.moisture_preference` has an invalid value")
        for key in ["drought_tolerance", "waterlogging_tolerance"]:
            if water.get(key) not in TOLERANCE_VALUES:
                fail(errors, path, f"`water.{key}` has an invalid value")
        if water.get("guidance_style") != "check_before_watering":
            fail(errors, path, "`water.guidance_style` must be check_before_watering")

    establishment = profile.get("establishment")
    if not isinstance(establishment, dict):
        fail(errors, path, "`establishment` must be an object")
    else:
        for key, values in ESTABLISHMENT_VALUES.items():
            if establishment.get(key) not in values:
                fail(errors, path, f"`establishment.{key}` has an invalid value")
        if establishment.get("month_guidance") != "location_dependent":
            fail(errors, path, "`establishment.month_guidance` must be location_dependent")

    if not isinstance(profile.get("source_refs"), dict):
        fail(errors, path, "`source_refs` must be an object")
    if not isinstance(profile.get("unknowns"), list):
        fail(errors, path, "`unknowns` must be a list")


def validate_pack(pack: Path, errors: list[str]) -> None:
    if not pack.is_dir():
        return
    if pack.name.startswith("_"):
        return

    for filename in REQUIRED_FILES:
        path = pack / filename
        if not path.exists():
            fail(errors, pack, f"missing required file `{filename}`")

    plant_data = None
    if (pack / "plant.json").exists():
        try:
            plant_data = json.loads((pack / "plant.json").read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            plant_data = None
        validate_plant_json(pack, errors)
    if isinstance(plant_data, dict):
        validate_vnext_profile(pack, plant_data, errors)

    for filename in REQUIRED_FILES:
        path = pack / filename
        if path.exists() and path.suffix == ".md":
            non_empty_markdown(path, errors)


def main() -> int:
    errors: list[str] = []
    if not PACK_ROOT.exists():
        print("No research-packs directory found.")
        return 0

    packs = [path for path in sorted(PACK_ROOT.iterdir()) if path.is_dir() and not path.name.startswith("_")]
    for pack in packs:
        validate_pack(pack, errors)

    if errors:
        print("Research pack validation failed:\n")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Research pack validation passed ({len(packs)} pack(s) checked).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
