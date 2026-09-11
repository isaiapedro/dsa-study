"""Create safe, local-only Python solution skeletons from catalog records."""

from __future__ import annotations

import re
from pathlib import Path

from dsa_study.storage import catalog_path, read_json


def create_solution(root: Path, problem_id: str) -> Path:
    document = read_json(catalog_path(root), {})
    problem = next((row for row in document.get("problems", []) if str(row.get("id")) == str(problem_id)), None)
    if not problem:
        raise RuntimeError(f"Problem {problem_id} is not in the local catalog. Run `dsa-study sync` first.")
    slug = re.sub(r"[^a-z0-9-]+", "-", str(problem.get("slug") or problem_id).lower()).strip("-")
    target = root / "solutions" / str(problem["difficulty"]).lower() / f'{problem["id"]}-{slug}'
    if target.exists():
        raise RuntimeError(f"Refusing to overwrite existing solution workspace: {target}")
    target.mkdir(parents=True)
    starter = problem.get("python_starter") or "class Solution:\n    pass\n"
    (target / "solution.py").write_text(starter.rstrip() + "\n", encoding="utf-8")
    (target / "test_solution.py").write_text(f'"""Tests for {problem["id"]}. {problem.get("title", "")}. Add cases manually.\n\nLeetCode examples vary by signature, so no runnable tests are inferred automatically.\n"""\n\n', encoding="utf-8")
    (target / "README.md").write_text(f'# {problem["id"]}. {problem.get("title", "Untitled")}\n\n- Difficulty: {problem.get("difficulty")}\n- Local catalog page: `site/problems/{problem.get("slug")}.html`\n', encoding="utf-8")
    return target
