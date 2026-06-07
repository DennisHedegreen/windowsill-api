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


def validate_pack(pack: Path, errors: list[str]) -> None:
    if not pack.is_dir():
        return
    if pack.name.startswith("_"):
        return

    for filename in REQUIRED_FILES:
        path = pack / filename
        if not path.exists():
            fail(errors, pack, f"missing required file `{filename}`")

    if (pack / "plant.json").exists():
        validate_plant_json(pack, errors)

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
