"""Command-line tools for the Phase 2 engineering scaffold."""

from __future__ import annotations

import argparse
from pathlib import Path

from .engineering_pilot import dump_result, reference_baseline, reference_invariant_problems, run_reference_pilot
from .io import load_data, repository_root
from .phase2_gate import decision_problems, live_pilot_problems, scaffold_problems
from .schema_validation import validate_file


def _root(value: str | None) -> Path:
    return Path(value).resolve() if value else repository_root()


def scaffold_check(root: Path) -> int:
    problems = scaffold_problems(root)
    if problems:
        print("Phase 2 scaffold is NOT ready:")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print("Phase 2 deterministic engineering scaffold is ready.")
    return 0


def decisions(root: Path) -> int:
    document = load_data(root / "governance/human-decisions/phase-2.yaml")
    problems = decision_problems(document, "live_pilot")
    if problems:
        print(f"Live-pilot Human Decision Gate remains closed ({len(problems)} issue(s)):")
        for problem in problems:
            print(f"  - {problem}")
        return 0
    print("All live-pilot human decisions are satisfied.")
    return 0


def live_check(root: Path) -> int:
    problems = live_pilot_problems(root)
    if problems:
        print("Live engineering pilot is NOT authorized:")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print("Live engineering pilot is authorized and configured.")
    return 0


def reference_check(root: Path, write: bool = False) -> int:
    config = load_data(root / "pilot/phase-2.yaml")
    scenario_path = root / config["reference_runner"]["scenario_file"]
    result_path = root / config["reference_runner"]["checked_result_file"]
    result = run_reference_pilot(scenario_path)
    problems = reference_invariant_problems(result)
    if problems:
        print("Reference pilot invariant failure:")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    if write:
        result_path.parent.mkdir(parents=True, exist_ok=True)
        result_path.write_text(dump_result(reference_baseline(result)), encoding="utf-8")
        print(f"Wrote {result_path}")
        return 0
    if not result_path.exists():
        print(f"Checked reference result is missing: {result_path}")
        return 1
    checked = load_data(result_path)
    if checked != reference_baseline(result):
        print("Checked reference result does not match deterministic regeneration.")
        return 1
    schema_issues = validate_file(result_path, root / "schemas/reference_pilot_result.schema.json")
    if schema_issues:
        print("Reference result schema validation failed:")
        for issue in schema_issues:
            print(f"  - {issue}")
        return 1
    print("Deterministic reference pilot regenerated and verified.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="goalevo-phase2")
    parser.add_argument("--root")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("scaffold-check")
    sub.add_parser("decisions")
    sub.add_parser("live-check")
    reference = sub.add_parser("reference-check")
    reference.add_argument("--write", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    root = _root(args.root)
    if args.command == "scaffold-check":
        code = scaffold_check(root)
    elif args.command == "decisions":
        code = decisions(root)
    elif args.command == "live-check":
        code = live_check(root)
    else:
        code = reference_check(root, write=args.write)
    raise SystemExit(code)


if __name__ == "__main__":
    main()
