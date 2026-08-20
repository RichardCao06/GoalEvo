from pathlib import Path

from goalevo_protocol.io import load_data
from goalevo_protocol.phase2_gate import decision_problems, live_pilot_problems, scaffold_problems
from goalevo_protocol.schema_validation import validate_file

ROOT = Path(__file__).resolve().parents[1]


def test_phase2_documents_match_schemas() -> None:
    assert validate_file(ROOT / "pilot/phase-2.yaml", ROOT / "schemas/engineering_pilot.schema.json") == []
    assert validate_file(ROOT / "governance/human-decisions/phase-2.yaml", ROOT / "schemas/phase2_human_decisions.schema.json") == []


def test_deterministic_scaffold_is_authorized() -> None:
    assert scaffold_problems(ROOT) == []


def test_live_pilot_remains_human_blocked() -> None:
    document = load_data(ROOT / "governance/human-decisions/phase-2.yaml")
    assert decision_problems(document, "live_pilot")
    assert live_pilot_problems(ROOT)
    assert any(problem.source == "P2D012" for problem in live_pilot_problems(ROOT))
