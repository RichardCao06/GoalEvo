## Summary

<!-- Describe the research or engineering change. -->

## Change class

- [ ] Capability / Harness only
- [ ] Evaluator
- [ ] Goal Discovery
- [ ] Goal Normative Change
- [ ] Autonomy
- [ ] Assurance
- [ ] Capability Envelope
- [ ] Research protocol or data semantics

**Governance tier:** `T0_LOW | T1_MEDIUM | T2_HIGH | T3_CRITICAL`

## Governance

- [ ] The change has one primary change class, or a bundle of atomic patches.
- [ ] Any Goal, Autonomy, Assurance, Capability Envelope, hypothesis, metric, Gold-label, or Sealed-Test change has explicit human approval.
- [ ] Proposer, implementer, evaluator, and approver roles are separated where required.
- [ ] Unfavorable results and failed runs are retained.
- [ ] Coverage and abstention behavior are reported when the change can alter deferral behavior.

## Validation

- [ ] `python -m goalevo_protocol.cli validate`
- [ ] `python -m goalevo_protocol.cli decisions`
- [ ] `python -m goalevo_protocol.cli pilot-check`
- [ ] `pytest -q`
- [ ] Confirmatory freeze is not claimed unless `freeze-check` passes

## Evidence and traceability

<!-- Link human decisions, work orders, fixtures, tests, and protocol sections. -->
