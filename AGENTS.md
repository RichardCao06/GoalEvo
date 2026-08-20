# GoalEvo Agent Instructions

This file applies to the entire repository. The governing documents are `docs/HUMAN_AGENT_COLLABORATION_CHARTER.md` and the Protocol v0.1 compatibility supplement `docs/HUMAN_AGENT_COLLABORATION_CHARTER_V0.1_AMENDMENT.md`.

## 1. Decision rights

Agents MAY generate alternatives, code, schemas, fixtures, tests, simulations, audits, and documentation.

Agents MUST NOT independently:

- change what counts as success;
- approve Goal, Autonomy, Assurance, or Capability Envelope changes;
- change H1–H3, primary estimands, denominators, non-inferiority margins, exclusion rules, or Gold labels;
- read or create access paths to Sealed Tests without an approved Work Order and Independent Custodian;
- delete unfavorable runs, rejected patches, regressions, or dissenting reviews;
- mark a protocol as pilot-locked/frozen or claim a hypothesis is supported without the corresponding Gate;
- approve their own normative or high-risk Patch.

All such changes require a recorded human decision and, where specified, independent review.

## 2. Required change classification

Every nontrivial change MUST identify one primary class:

- `CAPABILITY_PATCH`
- `EVALUATOR_PATCH`
- `GOAL_DISCOVERY`
- `GOAL_NORMATIVE_CHANGE`
- `AUTONOMY_CHANGE`
- `ASSURANCE_CHANGE`
- `CAPABILITY_ENVELOPE_CHANGE`

Cross-layer work MUST be split into atomic patches or commits and linked through a bundle or PR description.

## 3. Risk-tier escalation

- `T0_LOW`: no acceptance, permission, proof, or scope change;
- `T1_MEDIUM`: independent review required;
- `T2_HIGH`: verified authority and independent review required;
- `T3_CRITICAL`: conservative v0.1 default requires two distinct human approvals.

The exact T0–T3 thresholds are an engineering-pilot operationalization of D007. Changing their normative meaning requires a Protocol Amendment.

## 4. Mandatory escalation triggers

Stop and request a human decision when a change:

- expands an acceptance set;
- lowers evidence or sign-off requirements;
- expands tools, data, write, release authority, or certified capability scope;
- changes a blocking Human Decision;
- touches hidden goals, Gold labels, or Sealed material;
- creates an ambiguous taxonomy classification;
- can change the confirmatory conclusion.

## 5. Implementation rules

- Preserve raw evidence and derive metrics reproducibly.
- Keep Experimental Agent inputs isolated from hidden truth and audit data.
- Use deterministic validation whenever a rule can be expressed in code.
- Do not combine severe safety errors into a compensating aggregate score.
- Do not treat frequent or erroneous abstention as merely low utility; report it separately.
- Record versions, timestamps, effective times, source IDs, and content hashes.
- Keep proposer, implementer, evaluator, approver, and custodian distinct where required.

## 6. Required validation

Before proposing or publishing changes, run:

```bash
python -m goalevo_protocol.cli validate
python -m goalevo_protocol.cli decisions
python -m goalevo_protocol.cli pilot-check
pytest -q
```

For formal confirmatory authorization, also run:

```bash
python -m goalevo_protocol.cli freeze-check
```

Protocol v0.1 is expected to pass `pilot-check` and fail `freeze-check`. Never weaken either Gate merely to make CI green.

## 7. Pull requests

PR descriptions MUST state:

- change class and governance tier;
- human decisions affected;
- files and schemas changed;
- tests run;
- unresolved decisions or risks;
- whether the change is engineering-pilot, exploratory, or confirmatory.

A PR MUST remain Draft while its declared delivery Gate has not passed.
