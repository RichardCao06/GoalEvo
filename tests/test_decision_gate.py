from copy import deepcopy
from pathlib import Path

from goalevo_protocol.decision_gate import (
    confirmatory_decision_problems,
    decision_problems,
    freeze_problems,
    pilot_lock_problems,
)
from goalevo_protocol.io import load_data


ROOT = Path(__file__).resolve().parents[1]


def test_recorded_human_decisions_clear_engineering_pilot_gate() -> None:
    document = load_data(ROOT / "governance/human-decisions/phase-1.yaml")
    assert decision_problems(document) == []


def test_protocol_v0_1_is_pilot_locked() -> None:
    assert pilot_lock_problems(ROOT) == []


def test_confirmatory_gate_remains_closed_until_independent_roles_are_filled() -> None:
    document = load_data(ROOT / "governance/human-decisions/phase-1.yaml")
    problems = confirmatory_decision_problems(document)
    rendered = "\n".join(str(problem) for problem in problems)
    assert "methods_statistics_lead" in rendered
    assert "independent_custodian" in rendered
    assert "confirmatory_experiment has not been authorized" in rendered


def test_research_owner_is_required_for_engineering_pilot() -> None:
    document = deepcopy(load_data(ROOT / "governance/human-decisions/phase-1.yaml"))
    d012 = next(d for d in document["decisions"] if d["id"] == "D012")
    d012["role_assignments"]["research_owner"] = {
        "assignee": "",
        "status": "vacant",
        "required_before": "pilot",
    }
    assert any("research_owner" in problem.reason for problem in decision_problems(document))


def test_protocol_v0_1_is_not_confirmatory_freeze_eligible() -> None:
    problems = freeze_problems(ROOT)
    assert problems
    assert any("non-inferiority margin" in problem for problem in problems)
    assert any("sealed" in problem for problem in problems)
