"""Phase 2 engineering-pilot decision and authorization gates."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .io import load_data


@dataclass(frozen=True)
class Phase2Problem:
    source: str
    reason: str

    def __str__(self) -> str:
        return f"{self.source}: {self.reason}"


def _decisions(document: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(item.get("id")): item for item in document.get("decisions", [])}


def decision_problems(document: dict[str, Any], gate: str) -> list[Phase2Problem]:
    """Return unresolved human decisions for *gate*.

    `live_pilot` requires approve/modify for all associated decisions, except
    P2D012 which requires the explicit `authorize_live_pilot` value.
    """

    problems: list[Phase2Problem] = []
    seen: set[str] = set()
    for item in document.get("decisions", []):
        decision_id = str(item.get("id", "UNKNOWN"))
        if decision_id in seen:
            problems.append(Phase2Problem(decision_id, "duplicate decision id"))
        seen.add(decision_id)
        if gate not in (item.get("blocks") or []):
            continue

        value = item.get("decision")
        expected = {"approve", "modify"}
        if decision_id == "P2D012" and gate == "live_pilot":
            expected = {"authorize_live_pilot"}
        if value not in expected:
            problems.append(Phase2Problem(decision_id, f"decision is {value!r}; expected one of {sorted(expected)}"))
            continue
        if not str(item.get("approved_by", "")).strip():
            problems.append(Phase2Problem(decision_id, "approved_by is required"))
        if not str(item.get("approved_at", "")).strip():
            problems.append(Phase2Problem(decision_id, "approved_at is required"))
        if value == "modify" and not str(item.get("human_rationale", "")).strip():
            problems.append(Phase2Problem(decision_id, "modify requires a human rationale"))

    decisions = _decisions(document)
    for decision_id, required_roles in {
        "P2D008": ("coder_1", "coder_2", "adjudicator"),
        "P2D009": ("method_label_custodian",),
        "P2D011": ("pilot_approver", "independent_reviewer"),
        "P2D013": ("world_semantics_reviewer",),
    }.items():
        item = decisions.get(decision_id)
        if not item or gate not in (item.get("blocks") or []):
            continue
        if item.get("decision") not in {"approve", "modify", "authorize_live_pilot"}:
            continue
        roles = item.get("role_assignments") or {}
        missing = [role for role in required_roles if not str(roles.get(role, "")).strip()]
        if missing:
            problems.append(Phase2Problem(decision_id, f"missing role assignments: {', '.join(missing)}"))
    return problems


def scaffold_problems(root: Path) -> list[Phase2Problem]:
    config = load_data(root / "pilot/phase-2.yaml")
    decisions = load_data(root / "governance/human-decisions/phase-2.yaml")
    problems: list[Phase2Problem] = []

    if config.get("status") not in {"scaffold_ready", "live_ready", "running", "pilot_complete"}:
        problems.append(Phase2Problem("pilot/phase-2.yaml", "status is not scaffold-ready"))
    if config.get("authorized_scope") != "deterministic_reference_only":
        problems.append(Phase2Problem("pilot/phase-2.yaml", "scaffold must remain deterministic_reference_only"))
    if config.get("confirmatory_use") != "prohibited":
        problems.append(Phase2Problem("pilot/phase-2.yaml", "confirmatory use must be prohibited"))
    if config.get("sealed_test_status") != "not_created":
        problems.append(Phase2Problem("pilot/phase-2.yaml", "Phase 2 scaffold must not create a Sealed Test"))
    reference = config.get("reference_runner") or {}
    if reference.get("live_model_calls") is not False:
        problems.append(Phase2Problem("pilot/phase-2.yaml", "reference runner must make no live model calls"))
    if (config.get("live_pilot") or {}).get("authorized") is not False:
        problems.append(Phase2Problem("pilot/phase-2.yaml", "live pilot must remain unauthorized in scaffold"))

    p2d012 = _decisions(decisions).get("P2D012", {})
    if p2d012.get("decision") == "authorize_live_pilot":
        problems.append(Phase2Problem("P2D012", "scaffold branch must not contain live-pilot authorization"))
    return problems


def live_pilot_problems(root: Path) -> list[Phase2Problem]:
    config = load_data(root / "pilot/phase-2.yaml")
    decisions = load_data(root / "governance/human-decisions/phase-2.yaml")
    problems = decision_problems(decisions, "live_pilot")
    live = config.get("live_pilot") or {}
    if config.get("authorized_scope") != "live_engineering_pilot":
        problems.append(Phase2Problem("pilot/phase-2.yaml", "authorized_scope is not live_engineering_pilot"))
    if live.get("authorized") is not True:
        problems.append(Phase2Problem("pilot/phase-2.yaml", "live_pilot.authorized is not true"))
    for field in ("provider", "model_id", "model_version", "budget", "scale", "blinding"):
        if live.get(field) in {None, ""}:
            problems.append(Phase2Problem("pilot/phase-2.yaml", f"live_pilot.{field} is not configured"))
    if config.get("confirmatory_use") != "prohibited":
        problems.append(Phase2Problem("pilot/phase-2.yaml", "engineering pilot must remain non-confirmatory"))
    return problems
