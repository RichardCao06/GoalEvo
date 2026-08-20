"""Cross-artifact invariants that JSON Schema alone cannot express."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class InvariantIssue:
    artifact: str
    message: str

    def __str__(self) -> str:
        return f"{self.artifact}: {self.message}"


_TARGETS = {
    "CAPABILITY_PATCH": {"harness"},
    "EVALUATOR_PATCH": {"evaluator"},
    "GOAL_DISCOVERY": {"goal_contract"},
    "GOAL_NORMATIVE_CHANGE": {"goal_contract"},
    "AUTONOMY_CHANGE": {"autonomy_contract"},
    "ASSURANCE_CHANGE": {"assurance_contract", "capability_envelope"},
}


def validate_patch(patch: dict[str, Any]) -> list[InvariantIssue]:
    pid = patch.get("patch_id", "UNKNOWN_PATCH")
    issues: list[InvariantIssue] = []
    change_type = patch.get("change_type")
    target = patch.get("target_artifact")
    if change_type in _TARGETS and target not in _TARGETS[change_type]:
        issues.append(InvariantIssue(pid, f"{change_type} cannot target {target}"))

    evidence = patch.get("evidence_ids") or []
    authority = patch.get("authority_claim") or {}
    if change_type == "GOAL_DISCOVERY" and not evidence:
        issues.append(InvariantIssue(pid, "GOAL_DISCOVERY requires discovery evidence"))
    if change_type == "GOAL_NORMATIVE_CHANGE":
        if not patch.get("effective_time"):
            issues.append(InvariantIssue(pid, "GOAL_NORMATIVE_CHANGE requires effective_time"))
        if patch.get("status") in {"approved", "deployed"} and authority.get("status") != "verified":
            issues.append(InvariantIssue(pid, "approved/deployed normative change requires verified authority"))
        if patch.get("status") in {"approved", "deployed"} and not authority.get("evidence_ids"):
            issues.append(InvariantIssue(pid, "approved/deployed normative change requires authority evidence"))

    delta = patch.get("predicted_acceptance_delta") or {}
    if delta.get("newly_allowed_cases") and patch.get("risk_assessment", {}).get("severity") not in {"high", "critical"}:
        issues.append(InvariantIssue(pid, "acceptance expansion must be rated high or critical in the draft protocol"))
    return issues


def validate_review(review: dict[str, Any], patches: dict[str, dict[str, Any]]) -> list[InvariantIssue]:
    rid = review.get("decision_id", "UNKNOWN_REVIEW")
    issues: list[InvariantIssue] = []
    patch = patches.get(review.get("patch_id"))
    if patch is None:
        return [InvariantIssue(rid, "references unknown patch")]
    if review.get("sealed_accessed") is not False:
        issues.append(InvariantIssue(rid, "review must not access sealed test during Phase 1"))
    if review.get("decision") == "approve":
        if not review.get("independent_from_proposer"):
            issues.append(InvariantIssue(rid, "approved patch requires an independent reviewer"))
        if patch.get("change_type") in {"GOAL_NORMATIVE_CHANGE", "AUTONOMY_CHANGE", "ASSURANCE_CHANGE"} and not review.get("authority_valid"):
            issues.append(InvariantIssue(rid, "normative/high-risk approval requires valid authority"))
    return issues


def validate_snapshot(snapshot: dict[str, Any], patches: dict[str, dict[str, Any]]) -> list[InvariantIssue]:
    sid = snapshot.get("snapshot_id", "UNKNOWN_SNAPSHOT")
    issues: list[InvariantIssue] = []
    for patch_id in snapshot.get("applied_patch_ids", []):
        patch = patches.get(patch_id)
        if patch is None:
            issues.append(InvariantIssue(sid, f"applies unknown patch {patch_id}"))
        elif patch.get("status") not in {"approved", "deployed"}:
            issues.append(InvariantIssue(sid, f"applies patch {patch_id} with status {patch.get('status')}"))
    return issues


def validate_execution(execution: dict[str, Any]) -> list[InvariantIssue]:
    eid = execution.get("execution_id", "UNKNOWN_EXECUTION")
    issues: list[InvariantIssue] = []
    if execution.get("severe_false_pass") and not execution.get("false_pass"):
        issues.append(InvariantIssue(eid, "severe_false_pass requires false_pass"))
    if execution.get("infrastructure_failure") and execution.get("method_failure"):
        issues.append(InvariantIssue(eid, "failure cannot be both infrastructure and method failure"))
    if execution.get("abstained") != (execution.get("declared_status") == "abstain"):
        issues.append(InvariantIssue(eid, "abstained flag must match declared_status"))
    return issues


def validate_outcome(outcome: dict[str, Any]) -> list[InvariantIssue]:
    oid = f"outcome:{outcome.get('run_id')}:{outcome.get('generation')}"
    issues: list[InvariantIssue] = []
    if outcome.get("unauthorized_relaxations_deployed", 0) > outcome.get("unauthorized_relaxation_opportunities", 0):
        issues.append(InvariantIssue(oid, "deployed unauthorized relaxations exceed opportunities"))
    if outcome.get("unauthorized_relaxations_proposed", 0) > outcome.get("unauthorized_relaxation_opportunities", 0):
        issues.append(InvariantIssue(oid, "proposed unauthorized relaxations exceed opportunities"))
    if outcome.get("severe_false_passes", 0) > outcome.get("high_risk_tasks", 0):
        issues.append(InvariantIssue(oid, "severe false passes exceed high-risk tasks"))
    if outcome.get("legitimate_changes_correctly_adopted", 0) > outcome.get("legitimate_change_opportunities", 0):
        issues.append(InvariantIssue(oid, "adopted legitimate changes exceed opportunities"))
    return issues


def validate_fixture(bundle: dict[str, Any]) -> list[InvariantIssue]:
    issues: list[InvariantIssue] = []
    patches = {p["patch_id"]: p for p in bundle.get("patches", [])}
    for patch in patches.values():
        issues.extend(validate_patch(patch))
    for review in bundle.get("reviews", []):
        issues.extend(validate_review(review, patches))
    for snapshot in bundle.get("snapshots", []):
        issues.extend(validate_snapshot(snapshot, patches))
    for execution in bundle.get("executions", []):
        issues.extend(validate_execution(execution))
    for outcome in bundle.get("outcomes", []):
        issues.extend(validate_outcome(outcome))

    tasks = {task["task_id"]: task for task in bundle.get("tasks", [])}
    task_ids = set(tasks)
    snapshot_ids = {snapshot["snapshot_id"] for snapshot in bundle.get("snapshots", [])}
    execution_ids = {execution["execution_id"] for execution in bundle.get("executions", [])}
    for execution in bundle.get("executions", []):
        eid = execution.get("execution_id", "UNKNOWN")
        task = tasks.get(execution.get("task_id"))
        if task is None:
            issues.append(InvariantIssue(eid, "references unknown task"))
        else:
            declared = execution.get("declared_status")
            accepted = bool(task.get("oracle_acceptance"))
            expected_false_pass = declared == "success" and not accepted
            expected_false_block = declared == "failure" and accepted
            if bool(execution.get("false_pass")) != expected_false_pass:
                issues.append(InvariantIssue(eid, "false_pass flag is inconsistent with task oracle acceptance"))
            if bool(execution.get("false_block")) != expected_false_block:
                issues.append(InvariantIssue(eid, "false_block flag is inconsistent with task oracle acceptance"))
            if declared in {"success", "failure"}:
                expected_oracle = "fail" if (expected_false_pass or expected_false_block) else "pass"
                if execution.get("oracle_status") != expected_oracle:
                    issues.append(InvariantIssue(eid, f"oracle_status should be {expected_oracle}"))
        if execution.get("snapshot_id") not in snapshot_ids:
            issues.append(InvariantIssue(eid, "references unknown snapshot"))
    for outcome in bundle.get("outcomes", []):
        missing = sorted(set(outcome.get("source_execution_ids", [])) - execution_ids)
        if missing:
            issues.append(InvariantIssue(f"outcome:{outcome.get('run_id')}", f"references unknown executions: {missing}"))
    return issues
