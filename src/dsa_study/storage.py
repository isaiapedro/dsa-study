"""Filesystem layout for generated, intentionally untracked study material."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def project_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if (candidate / "pyproject.toml").exists() and (candidate / "manifest.yaml").exists():
            return candidate
    raise RuntimeError("Run this command inside the dsa_study project.")


def catalog_path(root: Path) -> Path:
    return root / "data" / "catalog.json"


def checkpoint_path(root: Path) -> Path:
    return root / ".dsa-study" / "sync-state.json"


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)
