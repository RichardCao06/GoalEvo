from pathlib import Path

from goalevo_protocol.io import load_data

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures/data-access-v0"


def test_data_access_world_has_effective_time_counterfactual() -> None:
    tasks = {item["task_id"]: item for item in load_data(FIXTURE / "tasks.yaml")}
    before = tasks["task-temp-12h-before-effective"]
    after = tasks["task-temp-12h-after-effective"]
    assert before["counterfactual_pair_id"] == after["counterfactual_pair_id"]
    assert before["oracle_expected_action"] == "approve"
    assert after["oracle_expected_action"] == "reject"


def test_unsafe_scope_and_goal_changes_are_retained_but_rejected() -> None:
    patches = {item["patch_id"]: item for item in load_data(FIXTURE / "patch_proposals.yaml")}
    assert patches["patch-data-access-permanent-unauthorized"]["status"] == "rejected"
    assert patches["patch-data-access-expand-write"]["change_type"] == "CAPABILITY_ENVELOPE_CHANGE"
    assert patches["patch-data-access-expand-write"]["status"] == "rejected"


def test_ambiguous_authority_is_escalated_not_silently_accepted() -> None:
    executions = {item["execution_id"]: item for item in load_data(FIXTURE / "executions.yaml")}
    record = executions["execution-data-ambiguous-policy-g1"]
    assert record["declared_status"] == "escalate"
    assert record["deferral_assessment"] == "justified"
