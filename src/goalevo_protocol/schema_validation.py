"""JSON Schema validation for GoalEvo protocol artifacts."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator, FormatChecker

from .io import load_data


@dataclass(frozen=True)
class ValidationIssue:
    path: str
    message: str

    def __str__(self) -> str:
        return f"{self.path}: {self.message}"


def _format_error_path(parts: Iterable[Any]) -> str:
    rendered = "$"
    for part in parts:
        rendered += f"[{part}]" if isinstance(part, int) else f".{part}"
    return rendered


def validate_instance(instance: Any, schema_path: Path, source: str = "instance") -> list[ValidationIssue]:
    schema = load_data(schema_path)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    issues: list[ValidationIssue] = []
    for error in sorted(validator.iter_errors(instance), key=lambda e: list(e.absolute_path)):
        issues.append(ValidationIssue(f"{source}{_format_error_path(error.absolute_path)[1:]}", error.message))
    return issues


def validate_file(data_path: Path, schema_path: Path, list_items: bool = False) -> list[ValidationIssue]:
    data = load_data(data_path)
    if list_items:
        if not isinstance(data, list):
            return [ValidationIssue(str(data_path), "expected a top-level list")]
        issues: list[ValidationIssue] = []
        for index, item in enumerate(data):
            issues.extend(validate_instance(item, schema_path, f"{data_path}[{index}]"))
        return issues
    return validate_instance(data, schema_path, str(data_path))
