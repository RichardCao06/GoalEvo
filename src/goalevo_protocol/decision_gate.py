"""Human decision and protocol freeze gates."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .io import load_data


@dataclass(frozen=True)
class DecisionProblem:
    decision_id: str
    reason: str

    def __str__(self) -> str:
        return f"{self.decision_id}: {self.reason}"


def decision_problems(decision_document: dict[str, Any]) -> list[DecisionProblem]:
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
        required_roles = {"research_owner", "methods_statistics_lead", "domain_lead", "data_steward", "independent_custodian"}
        missing = sorted(role for role in required_roles if not str(assignments.get(role, "")).strip())
        if missing:
            problems.append(DecisionProblem("D012", f"missing role assignments: {', '.join(missing)}"))
        if assignments.get("research_owner") and assignments.get("research_owner") == assignments.get("independent_custodian"):
            problems.append(DecisionProblem("D012", "research_owner and independent_custodian must not be the same sole identity"))
    return problems


def load_decision_problems(path: Path) -> list[DecisionProblem]:
    document = load_data(path)
    if not isinstance(document, dict):
        return [DecisionProblem("DOCUMENT", "decision document must be an object")]
    return decision_problems(document)


def freeze_problems(root: Path) -> list[str]:
    decision_path = root / "governance/human-decisions/phase-1.yaml"
    protocol_path = root / "protocol/phase-1.yaml"
    problems = [str(p) for p in load_decision_problems(decision_path)]
    protocol = load_data(protocol_path)
    if protocol.get("status") not in {"pilot_locked", "frozen"}:
        problems.append(f"protocol status is {protocol.get('status')!r}, expected 'pilot_locked' or 'frozen'")
    if not protocol.get("human_decision_gate"):
        problems.append("protocol human_decision_gate is false")
    if protocol.get("status") == "frozen" and not protocol.get("freeze_timestamp"):
        problems.append("frozen protocol requires freeze_timestamp")
    if protocol.get("noninferiority_margin", {}).get("status") == "frozen" and protocol.get("noninferiority_margin", {}).get("value") is None:
        problems.append("frozen noninferiority margin requires a numeric value")
    return problems
