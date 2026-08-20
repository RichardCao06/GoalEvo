## Summary

<!-- Describe the research or engineering change. -->

## Change class

- [ ] Capability / Harness only
- [ ] Evaluator
- [ ] Goal Discovery
- [ ] Goal Normative Change
- [ ] Autonomy
- [ ] Assurance / Capability Envelope
- [ ] Research protocol or data semantics

## Governance

- [ ] The change has one primary change class, or a bundle of atomic patches.
- [ ] Any Goal, Autonomy, Assurance, hypothesis, metric, Gold-label, or sealed-test change has explicit human approval.
- [ ] Proposer, implementer, evaluator, and approver roles are separated where required.
- [ ] Unfavorable results and failed runs are retained.

## Validation

- [ ] `python -m goalevo_protocol.cli validate`
- [ ] `pytest -q`
- [ ] Human Decision Gate reviewed
- [ ] Freeze eligibility is not claimed unless `freeze-check` passes

## Evidence and traceability

<!-- Link decisions, work orders, fixtures, tests, and protocol sections. -->
