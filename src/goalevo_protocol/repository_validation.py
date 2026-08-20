"""Repository-wide validation orchestration."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .invariants import validate_fixture
from .io import load_data
from .schema_validation import ValidationIssue, validate_file


_SINGLE_FILES = {
    "protocol/phase-1.yaml": "study_protocol.schema.json",
    "governance/human-decisions/phase-1.yaml": "human_decisions.schema.json",
}

_FIXTURE_SINGLE = {
    "world.yaml": "world_manifest.schema.json",
    "hidden_goal_v1.yaml": "goal_contract.schema.json",
    "hidden_goal_v2.yaml": "goal_contract.schema.json",
    "hidden_goal_timeline.yaml": "goal_truth_timeline.schema.json",
    "authority_graph.yaml": "authority_graph.schema.json",
}

_FIXTURE_LISTS = {
    "events.yaml": "event.schema.json",
    "tasks.yaml": "task_instance.schema.json",
    "patch_proposals.yaml": "patch_proposal.schema.json",
    "review_decisions.yaml": "review_decision.schema.json",
    "snapshots.yaml": "snapshot.schema.json",
    "runs.yaml": "run.schema.json",
    "executions.yaml": "task_execution.schema.json",
    "outcomes.yaml": "outcome_record.schema.json",
}


def validate_repository(root: Path) -> list[str]:
    issues: list[str] = []
    schema_dir = root / "schemas"
    for relative, schema_name in _SINGLE_FILES.items():
        for issue in validate_file(root / relative, schema_dir / schema_name):
            issues.append(str(issue))

    for fixture_dir in sorted((root / "fixtures").glob("*")):
        if not fixture_dir.is_dir():
            continue
        for name, schema_name in _FIXTURE_SINGLE.items():
            path = fixture_dir / name
            if path.exists():
                issues.extend(str(i) for i in validate_file(path, schema_dir / schema_name))
        for path in sorted(fixture_dir.glob("*goal_v*.yaml")):
            issues.extend(str(i) for i in validate_file(path, schema_dir / "goal_contract.schema.json"))
        for name, schema_name in _FIXTURE_LISTS.items():
            path = fixture_dir / name
            if path.exists():
                issues.extend(str(i) for i in validate_file(path, schema_dir / schema_name, list_items=True))

        bundle: dict[str, Any] = {}
        mapping = {
            "tasks": "tasks.yaml", "patches": "patch_proposals.yaml", "reviews": "review_decisions.yaml",
            "snapshots": "snapshots.yaml", "executions": "executions.yaml", "outcomes": "outcomes.yaml",
        }
        for key, filename in mapping.items():
            path = fixture_dir / filename
            bundle[key] = load_data(path) if path.exists() else []
        issues.extend(str(issue) for issue in validate_fixture(bundle))
    return issues
