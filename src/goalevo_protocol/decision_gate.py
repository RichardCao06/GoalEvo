"""Human decision, engineering-pilot lock, and confirmatory freeze gates."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from .io import load_data


@dataclass(frozen=True)
class DecisionProblem:
    decision_id: str
    reason: str

    def __str__(self) -> str:
        return f"{self.decision_id}: {self.reason}"


def _assignment_value(assignments: dict[str, Any], role: str) -> tuple[str, str]:
    raw = assignments.get(role, {})
    if isinstance(raw, str):
        return raw.strip(), "assigned" if raw.strip() else "vacant"
    if isinstance(raw, dict):
        return str(raw.get("assignee", "")).strip(), str(raw.get("status", "vacant"))
    return "", "vacant"


def _decision_core_problems(
    decision_document: dict[str, Any],
    *,
    require_confirmatory_roles: bool,
) -> list[DecisionProblem]:
    problems: list[DecisionProblem] = []
    seen: set[str] = set()
    for decision in decision_document.get("decisions", []):
        decision_id = decision.get("id", "UNKNOWN")
        if decision_id in seen:
            problems.append(DecisionProblem(decision_id, "duplicate decision id"))
        seen.add(decision_id)

        value = decision.get("decision")
        blocking = bool(decision.get("blocking"))
        if blocking and value in {"pending", "defer", "reject", None}:
            problems.append(DecisionProblem(decision_id, f"blocking decision is {value!r}"))
            continue

        if value in {"approve", "modify"}:
            if not str(decision.get("approved_by", "")).strip():
                problems.append(DecisionProblem(decision_id, "approved_by is required"))
            if not str(decision.get("approved_at", "")).strip():
                problems.append(DecisionProblem(decision_id, "approved_at is required"))
            if value == "modify" and not str(decision.get("human_rationale", "")).strip():
                problems.append(DecisionProblem(decision_id, "modify requires a human rationale"))
            if decision.get("implementation_status") != "applied":
                problems.append(DecisionProblem(decision_id, "approved decision has not been applied to artifacts"))
            if decision.get("independent_review_status") not in {"passed", "not_required"}:
                problems.append(DecisionProblem(decision_id, "independent review is not complete"))

    d012 = next((d for d in decision_document.get("decisions", []) if d.get("id") == "D012"), None)
    if d012 and d012.get("decision") in {"approve", "modify"}:
        assignments = d012.get("role_assignments") or {}
        pilot_roles = {"research_owner", "domain_lead", "data_steward"}
        for role in sorted(pilot_roles):
            assignee, status = _assignment_value(assignments, role)
            if not assignee or status not in {"assigned", "provisional"}:
                problems.append(DecisionProblem("D012", f"pilot role {role} is not assigned"))
        if d012.get("current_authorized_stage") not in {"engineering_pilot", "confirmatory_experiment"}:
            problems.append(DecisionProblem("D012", "current_authorized_stage does not permit an engineering pilot"))

        if require_confirmatory_roles:
            required_roles = {
                "research_owner",
                "methods_statistics_lead",
                "domain_lead",
                "data_steward",
                "independent_custodian",
            }
            resolved: dict[str, str] = {}
            for role in sorted(required_roles):
                assignee, status = _assignment_value(assignments, role)
                resolved[role] = assignee
                if not assignee or status != "assigned":
                    problems.append(DecisionProblem("D012", f"confirmatory role {role} is not independently assigned"))
            if resolved.get("research_owner") and resolved.get("research_owner") == resolved.get("independent_custodian"):
                problems.append(DecisionProblem("D012", "research_owner and independent_custodian must be distinct"))
            if d012.get("current_authorized_stage") != "confirmatory_experiment":
                problems.append(DecisionProblem("D012", "confirmatory_experiment has not been authorized"))
    return problems


def decision_problems(decision_document: dict[str, Any]) -> list[DecisionProblem]:
    """Return blockers for the Phase 1 engineering-pilot decision gate."""
    return _decision_core_problems(decision_document, require_confirmatory_roles=False)


def confirmatory_decision_problems(decision_document: dict[str, Any]) -> list[DecisionProblem]:
    """Return decision/role blockers for confirmatory use."""
    return _decision_core_problems(decision_document, require_confirmatory_roles=True)


def load_decision_problems(path: Path, *, confirmatory: bool = False) -> list[DecisionProblem]:
    document = load_data(path)
    if not isinstance(document, dict):
        return [DecisionProblem("DOCUMENT", "decision document must be an object")]
    fn = confirmatory_decision_problems if confirmatory else decision_problems
    return fn(document)


def _prefix(items: Iterable[DecisionProblem]) -> list[str]:
    return [str(item) for item in items]


def pilot_lock_problems(root: Path) -> list[str]:
    decision_path = root / "governance/human-decisions/phase-1.yaml"
    protocol_path = root / "protocol/phase-1.yaml"
    problems = _prefix(load_decision_problems(decision_path))
    protocol = load_data(protocol_path)
    if protocol.get("status") not in {"pilot_locked", "frozen"}:
        problems.append(f"protocol status is {protocol.get('status')!r}, expected 'pilot_locked' or 'frozen'")
    if protocol.get("authorized_scope") not in {"engineering_pilot", "confirmatory_experiment"}:
        problems.append("protocol does not authorize an engineering pilot")
    if not protocol.get("human_decision_gate"):
        problems.append("protocol human_decision_gate is false")
    if not protocol.get("pilot_lock_timestamp"):
        problems.append("pilot-locked protocol requires pilot_lock_timestamp")
    content_hash = str(protocol.get("content_hash", ""))
    if not content_hash.startswith("git-commit:"):
        problems.append("pilot-locked protocol requires a git-commit content attestation")

    manifest_path = root / str(protocol.get("pilot_lock_manifest", ""))
    if not manifest_path.exists():
        problems.append("pilot lock manifest is missing")
    else:
        manifest = load_data(manifest_path)
        if manifest.get("status") != "pilot_locked":
            problems.append("pilot lock manifest is not pilot_locked")
        semantic_commit = str(manifest.get("semantic_baseline_commit", ""))
        if not semantic_commit or semantic_commit == "pending":
            problems.append("pilot lock manifest lacks a semantic baseline commit")
        elif content_hash != f"git-commit:{semantic_commit}":
            problems.append("protocol content attestation does not match the pilot lock manifest")
    return problems


def freeze_problems(root: Path) -> list[str]:
    """Return blockers for the final confirmatory freeze, not merely the pilot lock."""
    decision_path = root / "governance/human-decisions/phase-1.yaml"
    protocol_path = root / "protocol/phase-1.yaml"
    protocol = load_data(protocol_path)
    problems = _prefix(load_decision_problems(decision_path, confirmatory=True))
    if protocol.get("status") != "frozen":
        problems.append(f"protocol status is {protocol.get('status')!r}, expected 'frozen'")
    if protocol.get("authorized_scope") != "confirmatory_experiment":
        problems.append("confirmatory_experiment scope is not authorized")
    if not protocol.get("freeze_timestamp"):
        problems.append("frozen protocol requires freeze_timestamp")
    margin = protocol.get("noninferiority_margin", {})
    if margin.get("status") != "frozen" or margin.get("value") is None:
        problems.append("confirmatory freeze requires a numeric frozen non-inferiority margin")
    if protocol.get("sealed_test_policy", {}).get("status") != "created_sealed":
        problems.append("confirmatory freeze requires a created and sealed final test")
    return problems
