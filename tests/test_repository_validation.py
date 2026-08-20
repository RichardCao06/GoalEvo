from pathlib import Path

from goalevo_protocol.repository_validation import validate_repository


ROOT = Path(__file__).resolve().parents[1]


def test_repository_draft_artifacts_validate() -> None:
    assert validate_repository(ROOT) == []
