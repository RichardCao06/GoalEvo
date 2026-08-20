from copy import deepcopy
from pathlib import Path

from goalevo_protocol.decision_gate import decision_problems, freeze_problems
from goalevo_protocol.io import load_data


ROOT = Path(__file__).resolve().parents[1]


def test_draft_has_unresolved_human_decisions() -> None:
    document = load_data(ROOT / "governance/human-decisions/phase-1.yaml")
    problems = decision_problems(document)
    assert problems
    assert any(problem.decision_id == "D001" for problem in problems)


def test_fully_signed_decision_document_can_clear_gate() -> None:
    document = deepcopy(load_data(ROOT / "governance/human-decisions/phase-1.yaml"))
    for decision in document["decisions"]:
        decision["decision"] = "approve"
        decision["human_rationale"] = "Approved for test."
        decision["approved_by"] = "human-owner"
        decision["approved_at"] = "2026-08-20T12:00:00Z"
        decision["implementation_status"] = "applied"
        decision["independent_review_status"] = "passed"
        if decision["id"] == "D012":
            decision["role_assignments"] = {
                "research_owner": "owner",
                "methods_statistics_lead": "methods",
                "domain_lead": "domain",
                "data_steward": "data",
                "independent_custodian": "custodian",
            }
    assert decision_problems(document) == []


def test_current_protocol_is_not_freeze_eligible() -> None:
    problems = freeze_problems(ROOT)
    assert problems
    assert any("protocol status" in problem for problem in problems)
