from pathlib import Path

from goalevo_protocol.engineering_pilot import reference_baseline, reference_invariant_problems, run_reference_pilot
from goalevo_protocol.io import load_data
from goalevo_protocol.schema_validation import validate_file

ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ROOT / "pilot/reference-scenarios/reference-pilot-v0.yaml"
RESULT = ROOT / "pilot/reference-results/reference-pilot-v0-summary.yaml"


def test_reference_pilot_is_deterministic_and_checked_in() -> None:
    generated = run_reference_pilot(SCENARIOS)
    assert reference_baseline(generated) == load_data(RESULT)
    assert reference_invariant_problems(generated) == []


def test_reference_result_matches_schema() -> None:
    assert validate_file(RESULT, ROOT / "schemas/reference_pilot_result.schema.json") == []


def test_reference_pilot_exercises_required_paths_without_claiming_evidence() -> None:
    generated = run_reference_pilot(SCENARIOS)
    result = reference_baseline(generated)
    summary = result["summary"]["by_method"]
    assert result["reference_only"] is True
    assert result["confirmatory_use"] == "prohibited"
    assert summary["M2"]["unauthorized_deployments"] > 0
    assert summary["M3"]["unauthorized_deployments"] == 0
    assert summary["M3"]["legitimate_adaptations"] > 0
    assert summary["M3"]["justified_deferrals"] > 0
