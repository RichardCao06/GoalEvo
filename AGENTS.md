# GoalEvo Agent Instructions

This file applies to the entire repository. The full governing document is `docs/HUMAN_AGENT_COLLABORATION_CHARTER.md`.

## 1. Decision rights

Agents MAY generate alternatives, code, schemas, fixtures, tests, simulations, audits, and documentation.

Agents MUST NOT independently:

- change what counts as success;
- approve Goal, Autonomy, Assurance, or Capability Envelope changes;
- change H1–H3, primary estimands, denominators, non-inferiority margins, exclusion rules, or Gold labels;
- read or create access paths to sealed tests without an approved Work Order;
- delete unfavorable runs, rejected patches, regressions, or dissenting reviews;
- mark a protocol as frozen or claim a hypothesis is supported;
- approve their own normative patch.

All such changes require a recorded human decision and, where specified, independent review.

## 2. Required change classification

Every nontrivial change MUST identify one primary class:

- `CAPABILITY_PATCH`
- `EVALUATOR_PATCH`
- `GOAL_DISCOVERY`
- `GOAL_NORMATIVE_CHANGE`
- `AUTONOMY_CHANGE`
- `ASSURANCE_CHANGE`

Cross-layer work MUST be split into atomic patches or commits and linked through a bundle or PR description.

## 3. Escalation triggers

Stop and request human decision when a change:

- expands an acceptance set;
- lowers evidence or sign-off requirements;
- expands tools, data, write, or release authority;
- changes a blocking Human Decision;
- touches hidden goals, Gold labels, or sealed material;
- creates an ambiguous taxonomy classification;
- can change the confirmatory conclusion.

## 4. Implementation rules

- Preserve raw evidence and derive metrics reproducibly.
- Keep Experimental Agent inputs isolated from hidden truth and audit data.
- Use deterministic validation whenever a rule can be expressed in code.
- Do not combine severe safety errors into a compensating aggregate score.
- Record versions, timestamps, effective times, source IDs, and content hashes.
- Keep proposer, implementer, evaluator, and approver distinct where required.

## 5. Required validation

Before proposing or publishing changes, run:

```bash
PYTHONPATH=src python -m goalevo_protocol.cli validate
PYTHONPATH=src pytest -q
PYTHONPATH=src python -m goalevo_protocol.cli decisions
```

`freeze-check` is expected to fail while the protocol is a draft. Never weaken the gate merely to make it pass.

## 6. Pull requests

PR descriptions MUST state:

- change class;
- human decisions affected;
- files and schemas changed;
- tests run;
- unresolved decisions or risks;
- whether the change is confirmatory or exploratory.

A Draft PR MUST remain Draft while blocking human decisions are unresolved.
