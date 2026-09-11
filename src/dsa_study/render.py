"""Dependency-free static HTML renderer for the local study catalog."""

from __future__ import annotations

import html
import hashlib
import re
from pathlib import Path
from typing import Any


def _page(title: str, body: str, *, home: str = "index.html") -> str:
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title><style>
body{{max-width:1100px;margin:2rem auto;padding:0 1rem;font:16px/1.5 system-ui,sans-serif;color:#17212b;background:#fafafa}}a{{color:#075985}}.topics,.tags{{display:flex;flex-wrap:wrap;gap:.45rem}}.topic,.tag{{padding:.22rem .55rem;border-radius:1rem;background:#e0f2fe;text-decoration:none}}.card{{background:white;border:1px solid #dbe3ea;border-radius:.5rem;padding:1rem;margin:.75rem 0}}.meta{{color:#52606d;font-size:.9rem}}.locked{{color:#9f1239}}pre{{overflow:auto;background:#17212b;color:#eef6ff;padding:1rem;border-radius:.35rem}}table{{border-collapse:collapse}}td,th{{border:1px solid #cbd5e1;padding:.4rem}}input{{width:100%;padding:.7rem;font:inherit;box-sizing:border-box}}
</style></head><body><p><a href="{home}">DSA Study</a></p>{body}</body></html>"""


def _problem_card(problem: dict[str, Any]) -> str:
    topics = "".join(f'<span class="tag">{html.escape(topic["name"])}</span>' for topic in problem.get("topics") or [])
    identifier = html.escape(problem.get("id") or "?")
    title = html.escape(problem.get("title") or "Untitled")
    status = problem.get("detail_status")
    heading = f'<a href="problems/{html.escape(_problem_filename(problem))}">{identifier}. {title}</a>' if problem.get("slug") else f"{identifier}. {title}"
    unavailable = '<span class="locked">Statement unavailable in public sync</span>' if status != "available" else ""
    return f'<article class="card problem" data-search="{html.escape((problem.get("title") or "").casefold())}"><h2>{heading}</h2><p class="meta">{html.escape(problem.get("difficulty") or "Unknown")} · {"Premium" if problem.get("paid_only") else "Public"} · {unavailable}</p><div class="tags">{topics}</div></article>'


def render_site(document: dict[str, Any], destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    problem_dir = destination / "problems"
    problem_dir.mkdir(exist_ok=True)
    problems = sorted(document.get("problems") or [], key=lambda row: (int(row["id"]) if str(row.get("id", "")).isdigit() else 10**9, row.get("slug", "")))
    topics = document.get("topics") or []
    topic_links = "".join(f'<a class="topic" href="#topic-{html.escape(topic["slug"])}">{html.escape(topic["name"])} ({topic["problem_count"]})</a>' for topic in topics)
    sections = []
    for topic in topics:
        matching = [row for row in problems if topic["slug"] in {tag.get("slug") for tag in row.get("topics") or []}]
        sections.append(f'<section id="topic-{html.escape(topic["slug"])}"><h2>{html.escape(topic["name"])} <small>({len(matching)})</small></h2>{"".join(_problem_card(row) for row in matching)}</section>')
    index_body = f"""<h1>DSA Study Catalog</h1><p class="meta">Synced {html.escape(document.get("synced_at") or "not yet")} · {len(problems)} problems · {len(topics)} official topics</p><input id="search" placeholder="Filter problems by title"><h2>Topics</h2><nav class="topics">{topic_links}</nav>{''.join(sections)}<script>document.querySelector('#search').addEventListener('input',e=>document.querySelectorAll('.problem').forEach(c=>c.hidden=!c.dataset.search.includes(e.target.value.toLowerCase())))</script>"""
    (destination / "index.html").write_text(_page("DSA Study Catalog", index_body), encoding="utf-8")
    for problem in problems:
        _render_problem(problem, problem_dir / _problem_filename(problem))


def _problem_filename(problem: dict[str, Any]) -> str:
    """Return a filename that cannot escape the generated problems directory."""
    slug = str(problem.get("slug") or "")
    if re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        return f"{slug}.html"
    digest = hashlib.sha256(slug.encode("utf-8")).hexdigest()[:16]
    return f"problem-{digest}.html"


def _render_problem(problem: dict[str, Any], path: Path) -> None:
    title = f'{problem.get("id", "?")}. {problem.get("title", "Untitled")}'
    tags = "".join(f'<span class="tag">{html.escape(topic["name"])}</span>' for topic in problem.get("topics") or [])
    if problem.get("detail_status") != "available":
        content = f'<p class="locked">This statement is unavailable through the public synchronization boundary ({html.escape(problem.get("detail_reason") or "not publicly readable")}).</p>'
    else:
        example_blocks = "".join(f'<h3>Example {index}</h3><p><strong>Input</strong></p><pre>{html.escape(example["input"])}</pre><p><strong>Output</strong></p><pre>{html.escape(example["output"])}</pre>' for index, example in enumerate(problem.get("examples") or [], 1))
        content = f'{problem.get("statement_html") or ""}<section><h2>Examples</h2>{example_blocks or "<p>No structured examples could be extracted; see statement above.</p>"}</section>'
    body = f'<h1>{html.escape(title)}</h1><p class="meta">{html.escape(problem.get("difficulty") or "Unknown")} · {"Premium" if problem.get("paid_only") else "Public"}</p><div class="tags">{tags}</div>{content}'
    path.write_text(_page(title, body, home="../index.html"), encoding="utf-8")
