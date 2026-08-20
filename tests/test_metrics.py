from pathlib import Path

from goalevo_protocol.io import load_data
from goalevo_protocol.metrics import aggregate_execution_utility, safe_rate, summarize_outcome


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures/reimbursement-v0"


def test_safe_rate_preserves_zero_denominator_as_missing() -> None:
    assert safe_rate(0, 0) is None
    assert safe_rate(1, 4) == 0.25


def test_outcome_summary_uses_predefined_denominators() -> None:
    outcome = load_data(FIXTURE / "outcomes.yaml")[1]
    summary = summarize_outcome(outcome)
    assert summary["unauthorized_relaxation_deployment_rate"] == 0.0
    assert summary["legitimate_change_adoption_rate"] == 1.0
    assert summary["hidden_goal_utility"] == 1.0


def test_execution_utility_uses_oracle_status() -> None:
    executions = load_data(FIXTURE / "executions.yaml")
    assert aggregate_execution_utility(executions) == 3 / 5
