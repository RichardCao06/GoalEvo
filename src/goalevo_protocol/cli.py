"""Command-line interface for GoalEvo protocol validation."""

from __future__ import annotations

import argparse
from pathlib import Path

from .decision_gate import freeze_problems, load_decision_problems, pilot_lock_problems
from .io import repository_root
from .repository_validation import validate_repository


def _root(value: str | None) -> Path:
    return Path(value).resolve() if value else repository_root()


def command_validate(root: Path) -> int:
    issues = validate_repository(root)
    if issues:
        print("Validation failed:")
        for issue in issues:
            print(f"  - {issue}")
        return 1
    print("Schema and cross-artifact validation passed.")
    return 0


def command_decisions(root: Path) -> int:
    path = root / "governance/human-decisions/phase-1.yaml"
    pilot = load_decision_problems(path)
    confirmatory = load_decision_problems(path, confirmatory=True)
    if pilot:
        print(f"Engineering-pilot Human Decision Gate remains open ({len(pilot)} issue(s)):")
        for problem in pilot:
            print(f"  - {problem}")
        return 0
    print("Engineering-pilot Human Decision Gate is satisfied.")
    if confirmatory:
        print(f"Confirmatory responsibility gate remains closed ({len(confirmatory)} issue(s)):")
        for problem in confirmatory:
            print(f"  - {problem}")
    else:
        print("Confirmatory human responsibility requirements are satisfied.")
    return 0


def _run_gate(root: Path, label: str, problems: list[str]) -> int:
    validation = validate_repository(root)
    all_problems = [*validation, *problems]
    if all_problems:
        print(f"Protocol is NOT eligible for {label}:")
        for problem in all_problems:
            print(f"  - {problem}")
        return 1
    print(f"Protocol is eligible for {label}.")
    return 0


def command_pilot_check(root: Path) -> int:
    return _run_gate(root, "engineering-pilot use", pilot_lock_problems(root))


def command_freeze_check(root: Path) -> int:
    return _run_gate(root, "confirmatory freeze", freeze_problems(root))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="goalevo")
    parser.add_argument("--root", help="Repository root; auto-detected by default")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate", help="Validate schemas and cross-artifact invariants")
    sub.add_parser("decisions", help="Report pilot and confirmatory human-decision gates")
    sub.add_parser("pilot-check", help="Fail unless Protocol v0.1 is eligible for engineering-pilot use")
    sub.add_parser("freeze-check", help="Fail unless all confirmatory-freeze prerequisites are met")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    root = _root(args.root)
    commands = {
        "validate": command_validate,
        "decisions": command_decisions,
        "pilot-check": command_pilot_check,
        "freeze-check": command_freeze_check,
    }
    raise SystemExit(commands[args.command](root))


if __name__ == "__main__":
    main()
