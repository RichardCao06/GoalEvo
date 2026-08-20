"""File loading helpers for protocol artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


def load_data(path: Path) -> Any:
    """Load YAML or JSON from *path*.

    Raises:
        ValueError: If the file extension is unsupported.
    """
    suffix = path.suffix.lower()
    text = path.read_text(encoding="utf-8")
    if suffix in {".yaml", ".yml"}:
        return yaml.safe_load(text)
    if suffix == ".json":
        return json.loads(text)
    raise ValueError(f"Unsupported data file: {path}")


def repository_root(start: Path | None = None) -> Path:
    """Find a GoalEvo repository root by walking upward from *start*."""
    current = (start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if (candidate / "pyproject.toml").exists() and (candidate / "schemas").is_dir():
            return candidate
    raise FileNotFoundError("Could not find GoalEvo repository root")
