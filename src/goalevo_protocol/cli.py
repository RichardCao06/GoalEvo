"""Command-line interface for GoalEvo protocol validation."""

from __future__ import annotations

import argparse
from pathlib import Path

from .decision_gate import freeze_problems, load_decision_problems
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
    problems = load_decision_problems(path)
    if problems:
        print(f"Human Decision Gate remains open ({len(problems)} issue(s)):")
        for problem in problems:
            print(f"  - {problem}")
        print("This is expected while the protocol is in draft status.")
        return 0
    print("All human decision requirements are satisfied.")
    return 0


def command_freeze_check(root: Path) -> int:
    validation = validate_repository(root)
    problems = [*validation, *freeze_problems(root)]
    if problems:
        print("Protocol is NOT eligible for freeze:")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print("Protocol is eligible for freeze.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="goalevo")
    parser.add_argument("--root", help="Repository root; auto-detected by default")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate", help="Validate schemas and cross-artifact invariants")
    sub.add_parser("decisions", help="Report unresolved human decisions")
    sub.add_parser("freeze-check", help="Fail unless all freeze prerequisites are met")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    root = _root(args.root)
    commands = {
        "validate": command_validate,
        "decisions": command_decisions,
        "freeze-check": command_freeze_check,
    }
    raise SystemExit(commands[args.command](root))


if __name__ == "__main__":
    main()
