from copy import deepcopy
from pathlib import Path

from goalevo_protocol.invariants import validate_patch, validate_review, validate_snapshot
from goalevo_protocol.io import load_data


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures/reimbursement-v0"


def _patches():
    return {p["patch_id"]: p for p in load_data(FIXTURE / "patch_proposals.yaml")}


def test_patch_target_must_match_change_type() -> None:
    patch = deepcopy(next(iter(_patches().values())))
    patch["target_artifact"] = "goal_contract"
    issues = validate_patch(patch)
    assert any("cannot target" in issue.message for issue in issues)


def test_deployed_normative_change_requires_verified_authority() -> None:
    patch = deepcopy(_patches()["patch-legitimate-emergency-cap-100"])
    patch["authority_claim"]["status"] = "invalid"
    issues = validate_patch(patch)
    assert any("verified authority" in issue.message for issue in issues)


def test_rejected_patch_cannot_appear_in_snapshot() -> None:
    snapshot = deepcopy(load_data(FIXTURE / "snapshots.yaml")[0])
    snapshot["applied_patch_ids"] = ["patch-unauthorized-threshold-5000"]
    issues = validate_snapshot(snapshot, _patches())
    assert any("status rejected" in issue.message for issue in issues)


def test_approved_review_requires_independence() -> None:
    review = deepcopy(load_data(FIXTURE / "review_decisions.yaml")[0])
    review["independent_from_proposer"] = False
    issues = validate_review(review, _patches())
    assert any("independent reviewer" in issue.message for issue in issues)
