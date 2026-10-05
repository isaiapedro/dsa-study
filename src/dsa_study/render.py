"""Dependency-free static HTML renderer for the local study catalog."""

from __future__ import annotations

import html
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from dsa_study.learning_blocks import load_learning_blocks, select_catalog_practice
from dsa_study.course import render_course


def _page(title: str, body: str, *, home: str = "index.html") -> str:
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title><style>
body{{max-width:1100px;margin:2rem auto;padding:0 1rem;font:16px/1.5 system-ui,sans-serif;color:#e5edf6;background:#0b1220}}a{{color:#7dd3fc}}.topics,.tags,.block-picker,.trace-controls,.array-diagram{{display:flex;flex-wrap:wrap;gap:.45rem}}.topic,.tag{{padding:.22rem .55rem;border-radius:1rem;background:#12304a;color:#d9f1ff;text-decoration:none}}.card,.study-block,.catalog-panel{{background:#111c2e;border:1px solid #29415e;border-radius:.5rem;padding:1rem;margin:.75rem 0}}.study-block{{border-top:4px solid #38bdf8}}.meta,.textbook-pages{{color:#a8bacd;font-size:.9rem}}.textbook-pages{{margin-top:-.5rem}}.locked{{color:#fda4af}}pre{{overflow:auto;background:#050a13;color:#e8f3ff;padding:1rem;border-radius:.35rem}}table{{border-collapse:collapse}}td,th{{border:1px solid #38516e;padding:.4rem}}input,textarea{{width:100%;padding:.7rem;font:inherit;box-sizing:border-box;background:#091321;color:#e5edf6;border:1px solid #45617f;border-radius:.3rem}}textarea{{min-height:5rem}}button{{font:inherit;padding:.45rem .7rem;border:1px solid #38bdf8;border-radius:.35rem;background:#10243b;color:#d9f1ff;cursor:pointer}}button:hover,button[aria-pressed="true"]{{background:#1479a8;color:white}}button:focus-visible,a:focus-visible,input:focus-visible,textarea:focus-visible,summary:focus-visible{{outline:3px solid #fbbf24;outline-offset:2px}}.visual{{background:#0d2136;border:1px solid #315a7d;padding:1rem;border-radius:.35rem}}.state{{border-left:4px solid #38bdf8;padding:.5rem .75rem;background:#101d2d;margin:.5rem 0}}.state[hidden],.study-block[hidden],.catalog-panel[hidden]{{display:none}}.cell{{min-width:2.8rem;padding:.45rem;border:1px solid #4a81aa;border-radius:.25rem;text-align:center;background:#132a42}}.cell.active{{border:3px solid #fbbf24;background:#27415b}}.bucket{{display:grid;grid-template-columns:5rem 1fr;gap:.5rem;margin:.3rem 0;padding:.35rem;background:#13243a;border-radius:.25rem}}.entry{{display:inline-block;margin:.15rem;padding:.2rem .4rem;border-radius:1rem;background:#27415b}}.pointer-note{{font-weight:600;color:#7dd3fc}}.question{{border-top:1px solid #29415e;padding-top:.75rem;margin-top:1rem}}.question label{{display:block;font-weight:600;margin-bottom:.35rem}}.callout{{background:#17273b;padding:.75rem;border-radius:.35rem}}.sr-only{{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}}@media (prefers-reduced-motion: reduce){{*,*::before,*::after{{animation-duration:.01ms!important;animation-iteration-count:1!important;scroll-behavior:auto!important;transition-duration:.01ms!important}}}}
</style></head><body><p><a href="{home}">DSA Study</a></p>{body}</body></html>"""


def _problem_card(problem: dict[str, Any]) -> str:
    topics = "".join(f'<span class="tag">{html.escape(topic["name"])}</span>' for topic in problem.get("topics") or [])
    identifier = html.escape(problem.get("id") or "?")
    title = html.escape(problem.get("title") or "Untitled")
    status = problem.get("detail_status")
    heading = f'<a href="problems/{html.escape(_problem_filename(problem))}">{identifier}. {title}</a>' if problem.get("slug") else f"{identifier}. {title}"
    unavailable = '<span class="locked">Statement unavailable in public sync</span>' if status != "available" else ""
    return f'<article class="card problem" data-search="{html.escape((problem.get("title") or "").casefold())}"><h2>{heading}</h2><p class="meta">{html.escape(problem.get("difficulty") or "Unknown")} · {"Premium" if problem.get("paid_only") else "Public"} · {unavailable}</p><div class="tags">{topics}</div></article>'


def render_site(document: dict[str, Any], destination: Path, *, learning_blocks: list[dict[str, Any]] | None = None) -> None:
    """Render public catalog records and authored, non-persistent learning blocks.

    Responses to the block prompts remain solely in browser form controls: the
    generated page has no form submission, storage, or network behaviour.
    """
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
    blocks = load_learning_blocks() if learning_blocks is None else learning_blocks
    study_area = render_course(destination, _page) + _render_study_area(blocks, problems)
    index_body = f"""{study_area}<section class="catalog-panel" id="catalog-panel" hidden><h1>DSA Study Catalog</h1><p class="meta">Synced {html.escape(document.get("synced_at") or "not yet")} · {len(problems)} problems · {len(topics)} official topics</p><label class="sr-only" for="search">Filter problems by title</label><input id="search" placeholder="Filter problems by title"><h2>Topics</h2><nav class="topics">{topic_links}</nav>{''.join(sections)}</section><button type="button" id="catalog-toggle" aria-controls="catalog-panel" aria-expanded="false">Show full problem list</button><script>const catalog=document.querySelector('#catalog-panel'),toggle=document.querySelector('#catalog-toggle');toggle.addEventListener('click',()=>{{catalog.hidden=!catalog.hidden;toggle.setAttribute('aria-expanded',String(!catalog.hidden));toggle.textContent=catalog.hidden?'Show full problem list':'Hide full problem list';if(!catalog.hidden)catalog.querySelector('#search').focus();}});document.querySelector('#search').addEventListener('input',e=>document.querySelectorAll('.problem').forEach(c=>c.hidden=!c.dataset.search.includes(e.target.value.toLowerCase())))</script>"""
    (destination / "index.html").write_text(_page("DSA Study Catalog", index_body), encoding="utf-8")
    for problem in problems:
        _render_problem(problem, problem_dir / _problem_filename(problem))


def _text(value: Any, default: str = "") -> str:
    """Return authored scalar text without permitting markup in static pages."""
    return html.escape(str(value if value is not None else default))


def _render_study_area(blocks: list[dict[str, Any]], problems: list[dict[str, Any]]) -> str:
    if not blocks:
        return ""
    choices = "".join(
        f'<button type="button" class="block-choice" data-block="{index}" aria-pressed="{'true' if index == 0 else 'false'}">{_text(block.get("sequence", index + 1))}. {_text(block.get("title", "Untitled block"))}</button>'
        for index, block in enumerate(blocks)
    )
    rendered = "".join(_render_learning_block(block, index, problems) for index, block in enumerate(blocks))
    return f'<section aria-labelledby="study-heading"><h1 id="study-heading">Interactive examples</h1><p>Choose an example and predict each step before revealing it.</p><nav class="block-picker" aria-label="Study blocks">{choices}</nav>{rendered}</section>{_study_script()}'


def _render_learning_block(block: dict[str, Any], index: int, problems: list[dict[str, Any]]) -> str:
    title = _text(block.get("title", "Untitled block"))
    module = str(block.get("course_module", ""))
    module_link = f'<p><a href="course/{module}.html">Read the full lesson</a></p>' if re.fullmatch(r"[0-9]{2}-[a-z-]+", module) else ""
    target = _text(block.get("target", block.get("outcomes", "")))
    visual = block.get("visual") or {}
    states = visual.get("states") or []
    state_markup = "".join(_render_trace_state(state, state_index, str(visual.get("kind") or "")) for state_index, state in enumerate(states)) or '<p class="state">No trace states have been authored yet.</p>'
    state_choice = _render_trace_choice(states, index)
    questions = block.get("questions") or []
    question_markup = "".join(_render_question(question, index, question_index) for question_index, question in enumerate(questions))
    hidden = "" if index == 0 else " hidden"
    return f'''<article class="study-block" data-study-block="{index}"{hidden} aria-labelledby="block-title-{index}">
<h2 id="block-title-{index}" tabindex="-1">{title}</h2>
{module_link}
<p>{target}</p><p><strong>Time and memory:</strong> {_text(block.get("expected_complexity"))}</p>
<section><h3>The idea</h3><p>{_text(block.get("theory"))}</p></section>
<figure class="visual" aria-labelledby="visual-title-{index}"><figcaption id="visual-title-{index}"><strong>{_text(visual.get("label", "State trace"))}</strong> · {_text(visual.get("prediction_checkpoint"))}</figcaption>
<p class="meta">Current state: <span data-current-state="{index}" aria-live="polite">1 of {len(states)}</span></p><p class="meta" data-motion-status="{index}">Playback is available; use Next, Previous, or Reset for direct control.</p>{state_markup}{state_choice}
<div class="trace-controls" aria-label="Trace controls"><button type="button" data-trace-action="play" data-trace="{index}">Play</button><button type="button" data-trace-action="pause" data-trace="{index}">Pause</button><button type="button" data-trace-action="previous" data-trace="{index}">Previous</button><button type="button" data-trace-action="step" data-trace="{index}">Next</button><button type="button" data-trace-action="reset" data-trace="{index}">Reset</button></div></figure>
<section><h3>Worked example</h3>{_render_activity(block.get("worked_example"))}</section>
<section><h3>Complete the next step</h3>{_render_activity(block.get("faded_scaffold"))}</section>
{_render_curriculum_context(block.get("curriculum_context"))}
{_render_pre_code_checkpoint(block.get("pre_code_checkpoint"), index)}
<section><h3>Independent practice</h3>{_render_activity(block.get("independent_practice"))}</section>
{_render_bridge_card(block.get("bridge_card"))}
{_render_catalog_practice(block, index, problems)}
<section aria-labelledby="prompts-{index}"><h3 id="prompts-{index}">Check your understanding</h3>{question_markup}</section>
<section><h3>Feedback checklist</h3><ul>{''.join(f'<li>{_text(item)}</li>' for item in block.get("feedback_checklist", []))}</ul><h3>Exit summary</h3><p>{_text(block.get("exit_summary"))}</p></section>
</article>'''


def _render_catalog_practice(block: dict[str, Any], block_index: int, problems: list[dict[str, Any]]) -> str:
    """Render transparent catalog routing and local-only interview prompts."""
    mapping = block.get("catalog_practice")
    prompts = block.get("interview_prompts") or []
    if not isinstance(mapping, dict) or not prompts:
        return ""
    selected = select_catalog_practice(block, problems)
    constraints = "".join(f"<li>{_text(item)}</li>" for item in mapping.get("constraints") or [])
    problems_markup = "".join(
        f'<li><a href="problems/{_text(_problem_filename(problem))}">{_text(problem.get("id", "?"))}. {_text(problem.get("title", "Untitled"))}</a> <span class="meta">{_text(problem.get("difficulty", "Unknown"))}</span></li>'
        for problem in selected
    ) or "<li>No synchronized catalog problem currently matches these declared tags. Sync the public catalog, then rebuild.</li>"
    prompt_markup = "".join(
        f'''<div class="question"><label for="interview-{block_index}-{prompt_index}"><strong>{_text(prompt.get("label"))}:</strong> {_text(prompt.get("prompt"))}</label>
<textarea id="interview-{block_index}-{prompt_index}" name="interview-{block_index}-{prompt_index}" autocomplete="off"></textarea></div>'''
        for prompt_index, prompt in enumerate(prompts)
        if isinstance(prompt, dict)
    )
    return f'''<section aria-labelledby="catalog-practice-{block_index}"><h3 id="catalog-practice-{block_index}">Focused catalog practice</h3>
<p class="callout">Practice <strong>{_text(mapping.get("technique"))}</strong>.</p>
<p><strong>Apply when:</strong></p><ul>{constraints}</ul><p><strong>Candidate problems:</strong></p><ol>{problems_markup}</ol>
<h4>Interview practice prompts</h4><p class="meta">Draft answers here before coding. They stay only in this page and are not saved.</p>{prompt_markup}</section>'''


def _render_curriculum_context(context: Any) -> str:
    """Render declared prerequisite and selection relationships as text."""
    if not isinstance(context, dict):
        return ""
    prerequisites = context.get("prerequisites") or ["None for this entry block"]
    dimensions = context.get("selection_dimensions") or []
    return f'''<details><summary>Related ideas</summary>
<p><strong>Part of:</strong> {_text(context.get("part_of"))}</p>
<p><strong>Prerequisites:</strong> {_text("; ".join(map(str, prerequisites)))}</p>
<p><strong>Choose this when:</strong> {_text("; ".join(map(str, dimensions)))}</p></details>'''


def _render_pre_code_checkpoint(checkpoint: Any, block_index: int) -> str:
    """Place a concise reasoning gate immediately before independent coding."""
    if not isinstance(checkpoint, dict):
        return ""
    prompts = checkpoint.get("prompts") or []
    fields = "".join(
        f'''<div class="question"><label for="pre-code-{block_index}-{prompt_index}">{_text(prompt.get("label", prompt.get("lens", "Plan"))) }: {_text(prompt.get("prompt"))}</label>
<textarea id="pre-code-{block_index}-{prompt_index}" name="pre-code-{block_index}-{prompt_index}" autocomplete="off"></textarea></div>'''
        for prompt_index, prompt in enumerate(prompts)
        if isinstance(prompt, dict)
    )
    return f'''<section aria-labelledby="pre-code-heading-{block_index}"><h3 id="pre-code-heading-{block_index}">Plan your solution</h3>
<p class="callout">{_text(checkpoint.get("purpose", "Plan the representation and correctness argument before coding."))}</p>{fields}</section>'''


def _render_bridge_card(card: Any) -> str:
    """Render an optional advanced connection without expanding the core block."""
    if not isinstance(card, dict):
        return ""
    return f'''<aside class="callout"><h3>Advanced bridge</h3><p><strong>{_text(card.get("title"))}</strong></p>
<p>{_text(card.get("connection"))}</p><p><strong>Question:</strong> {_text(card.get("question"))}</p></aside>'''


def _render_trace_state(state: Any, state_index: int, kind: str = "") -> str:
    if isinstance(state, dict):
        label = _text(state.get("label", f"State {state.get('step', state_index + 1)}"))
        detail = _text(state.get("description", state.get("message", state.get("content", ""))))
        diagram = _render_diagram(state, kind)
    else:
        label, detail, diagram = f"State {state_index + 1}", _text(state), ""
    hidden = "" if state_index == 0 else " hidden"
    return f'<div class="state" data-trace-state="{state_index}"{hidden}><strong>{label}</strong><div class="trace-diagram" aria-label="Visual state {label}">{diagram}</div><p>{detail}</p></div>'


def _render_trace_choice(states: list[Any], block_index: int) -> str:
    """Render a bounded native state picker that remains browser-memory only."""
    if len(states) < 2:
        return ""
    choices = []
    for state_index, state in enumerate(states[:5]):
        raw_label = state.get("label", f"State {state.get('step', state_index + 1)}") if isinstance(state, dict) else f"State {state_index + 1}"
        checked = " checked" if state_index == 0 else ""
        choices.append(f'<label><input type="radio" name="trace-choice-{block_index}" value="{state_index}" data-trace-choice="{block_index}"{checked}> {_text(raw_label)}</label>')
    return f'''<fieldset data-trace-choices="{block_index}"><legend>Choose an authored state</legend>
<p class="meta">This optional prediction control stays in this browser tab and is not saved.</p>{"".join(choices)}</fieldset>'''


def _render_diagram(state: dict[str, Any], kind: str) -> str:
    """Render a small semantic diagram; retain a text equivalent in the state message."""
    if kind in {"indexed-array-trace", "two-pointer-trace"} and isinstance(state.get("array", state.get("values")), list):
        values = state.get("array", state.get("values"))
        active = {state.get("i"), state.get("left"), state.get("right")}
        cells = "".join(f'<span class="cell{" active" if index in active else ""}"><small>{index}</small><br>{_text(value)}</span>' for index, value in enumerate(values))
        pointers = " · ".join(f'{name} = {_text(state[name])}' for name in ("i", "left", "right", "sum") if name in state)
        return f'<div class="array-diagram" aria-label="Indexed values">{cells}</div><p class="pointer-note">{pointers}</p>'
    if kind == "hash-bucket-trace" and isinstance(state.get("buckets"), dict):
        buckets = "".join(f'<div class="bucket"><strong>bucket {_text(bucket)}</strong><span>{"".join(f"<span class=\"entry\">{_text(entry)}</span>" for entry in entries) or "empty"}</span></div>' for bucket, entries in state["buckets"].items())
        lookup = f'<p class="pointer-note">lookup: {_text(state["lookup"])}</p>' if state.get("lookup") else ""
        return f'<div aria-label="Hash buckets">{buckets}</div>{lookup}'
    primitive = kind.casefold().replace("_", "-")
    if primitive in {"binary-search-interval", "binary-search", "binary-interval-trace", "binary-search-interval-trace"}:
        return _render_binary_search_interval(state)
    if primitive in {"linked-rewiring", "linked-list-rewiring", "linked-list-trace", "linked-list-rewire-trace"}:
        return _render_linked_rewiring(state)
    if primitive in {"stack-queue-state", "stack-queue-trace", "stack-queue", "worklist-order-trace"}:
        return _render_stack_queue_state(state)
    if primitive in {"tree-returns", "tree-return-trace", "tree-trace"}:
        return _render_tree_returns(state)
    if primitive in {"graph-frontiers", "graph-frontier", "graph-trace", "graph-frontier-trace"}:
        return _render_graph_frontier(state)
    if primitive in {"dp-dependencies", "dynamic-programming-dependencies", "dp-trace", "dp-dependency-trace"}:
        return _render_dp_dependencies(state)
    return _text({key: value for key, value in state.items() if key not in {"label", "description", "message", "content"}})


def _table(caption: str, headers: list[str], rows: list[list[Any]]) -> str:
    """Build an escaped, textual equivalent for an instructional diagram."""
    head = "".join(f"<th scope=\"col\">{_text(header)}</th>" for header in headers)
    body = "".join("<tr>" + "".join(f"<td>{_text(value)}</td>" for value in row) + "</tr>" for row in rows)
    return f'<table class="diagram-table"><caption>{_text(caption)}</caption><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>'


def _render_binary_search_interval(state: dict[str, Any]) -> str:
    values = state.get("values", state.get("array", []))
    if not isinstance(values, list):
        values = []
    low, high, mid = state.get("low", state.get("left")), state.get("high", state.get("right")), state.get("mid", state.get("middle"))
    rows = [[index, value, ", ".join(name for name, point in (("low", low), ("mid", mid), ("high", high)) if point == index) or "outside interval"] for index, value in enumerate(values)]
    note = " · ".join(f"{name} = {value}" for name, value in (("low", low), ("mid", mid), ("high", high), ("target", state.get("target"))) if value is not None)
    return _table("Binary-search interval (inclusive bounds)", ["Index", "Value", "Role"], rows) + f'<p class="pointer-note">{_text(note)}</p>'


def _render_linked_rewiring(state: dict[str, Any]) -> str:
    nodes = state.get("nodes", state.get("list", state.get("links", [])))
    rows: list[list[Any]] = []
    if isinstance(nodes, dict):
        nodes = [{"id": node, "next": successor} for node, successor in nodes.items()]
    if isinstance(nodes, list):
        for index, node in enumerate(nodes):
            node = node if isinstance(node, dict) else {"value": node}
            identity = node.get("id", node.get("name", index))
            rows.append([identity, node.get("value", node.get("val", "")), node.get("next", "null"), node.get("role", "")])
    pointers = ", ".join(f"{name} → {state[name]}" for name in ("head", "previous", "current", "next") if name in state)
    return _table("Linked nodes and next references", ["Node", "Value", "Next", "Role"], rows) + f'<p class="pointer-note">{_text(pointers)}</p>'


def _render_stack_queue_state(state: dict[str, Any]) -> str:
    stack = state.get("stack")
    queue = state.get("queue")
    parts = []
    if isinstance(stack, list):
        rows = [[index, value, "top" if index == len(stack) - 1 else ""] for index, value in enumerate(stack)]
        parts.append(_table("Stack state; the top is the removal end", ["Position", "Item", "Role"], rows))
    items = queue if isinstance(queue, list) else state.get("items", [])
    if isinstance(items, list):
        rows = [[index, value, "front" if index == 0 else "rear" if index == len(items) - 1 else ""] for index, value in enumerate(items)]
        parts.append(_table("Queue state; front leaves and rear receives", ["Position", "Item", "Role"], rows))
    next_items = " · ".join(f"{name.replace('_', ' ')}: {state[name]}" for name in ("stack_next", "queue_next") if name in state)
    return "".join(parts) + (f'<p class="pointer-note">{_text(next_items)}</p>' if next_items else "")


def _render_tree_returns(state: dict[str, Any]) -> str:
    nodes = state.get("nodes", state.get("tree", []))
    rows: list[list[Any]] = []
    if isinstance(nodes, dict):
        nodes = [{"node": key, **(value if isinstance(value, dict) else {"value": value})} for key, value in nodes.items()]
    if isinstance(nodes, list):
        for index, node in enumerate(nodes):
            node = node if isinstance(node, dict) else {"value": node}
            rows.append([node.get("node", node.get("id", index)), node.get("value", node.get("val", "")), node.get("left", "—"), node.get("right", "—"), node.get("return", node.get("result", "pending"))])
    elif "node" in state:
        rows.append([state["node"], state.get("value", state["node"]), state.get("left_return", "—"), state.get("right_return", "—"), state.get("return_value", "pending")])
    return _table("Tree calls and returned values", ["Node", "Value", "Left", "Right", "Return"], rows)


def _render_graph_frontier(state: dict[str, Any]) -> str:
    frontier = state.get("frontier", state.get("queue", state.get("stack", [])))
    frontier = frontier if isinstance(frontier, list) else []
    visited = state.get("visited", [])
    visited_text = ", ".join(map(str, visited)) if isinstance(visited, list) else str(visited)
    edges = state.get("edges", state.get("adjacency", {}))
    edge_rows = [[node, ", ".join(map(str, neighbors if isinstance(neighbors, list) else [neighbors]))] for node, neighbors in edges.items()] if isinstance(edges, dict) else []
    return _table("Graph frontier order", ["Position", "Vertex"], [[index, node] for index, node in enumerate(frontier)]) + f'<p class="pointer-note">Visited: {_text(visited_text)}</p>' + _table("Known outgoing edges", ["Vertex", "Neighbors"], edge_rows)


def _render_dp_dependencies(state: dict[str, Any]) -> str:
    cells = state.get("cells", state.get("table", state.get("states", [])))
    rows: list[list[Any]] = []
    if isinstance(cells, dict):
        cells = [{"state": key, **(value if isinstance(value, dict) else {"value": value})} for key, value in cells.items()]
    if isinstance(cells, list):
        for index, cell in enumerate(cells):
            cell = cell if isinstance(cell, dict) else {"value": cell}
            dependencies = cell.get("depends_on", cell.get("dependencies", ""))
            if isinstance(dependencies, list):
                dependencies = ", ".join(map(str, dependencies))
            rows.append([cell.get("state", cell.get("id", index)), cell.get("value", ""), dependencies, cell.get("decision", cell.get("transition", ""))])
    return _table("Dynamic-programming states and dependencies", ["State", "Value", "Depends on", "Decision"], rows)


def _render_activity(activity: Any) -> str:
    if not isinstance(activity, dict):
        return f'<p class="callout">{_text(activity)}</p>'
    parts = []
    for label, value in activity.items():
        if label in {"evidence", "stop_rule"}:
            continue
        if isinstance(value, list):
            value_markup = f'<pre>{_text(chr(10).join(map(str, value)))}</pre>'
        else:
            value_markup = f'<p>{_text(value)}</p>'
        if label == "expected_focus":
            parts.append(f'<details><summary>Check your answer</summary>{value_markup}</details>')
        else:
            title = {"input": "Example", "model": "Step by step", "boundary_test": "Smallest case", "prompt": "Try this", "pseudocode": "Complete the steps", "exercise": "Your turn"}.get(label, label.replace("_", " ").title())
            parts.append(f'<div class="callout"><strong>{_text(title)}</strong>{value_markup}</div>')
    return "".join(parts)


def _render_question(question: dict[str, Any], block_index: int, index: int) -> str:
    prompt = _text(question.get("prompt", "Write your response."))
    feedback = _text(question.get("feedback", "Compare your answer with the invariant and trace."))
    kind = _text(question.get("kind", "reflection"))
    return f'''<div class="question"><label for="answer-{block_index}-{index}">{index + 1}. {prompt}</label>
<textarea id="answer-{block_index}-{index}" name="answer-{block_index}-{index}" data-answer-kind="{kind}" autocomplete="off"></textarea>
<details><summary>Reveal feedback</summary><p>{feedback}</p></details></div>'''


def _study_script() -> str:
    """Client-only controls; deliberately avoid storage and network APIs."""
    return '''<script>(() => {
const timers = new Map();
const motionPreference = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)') : null;
function applyMotionPreference() {
  const reduceMotion = Boolean(motionPreference && motionPreference.matches);
  if (reduceMotion) [...timers.keys()].forEach(pause);
  document.querySelectorAll('[data-trace-action="play"]').forEach(button => {
    button.disabled = reduceMotion;
    button.setAttribute('aria-disabled', String(reduceMotion));
  });
  document.querySelectorAll('[data-motion-status]').forEach(status => {
    status.textContent = reduceMotion
      ? 'Reduced motion is active. Playback is disabled; use Next, Previous, or Reset for direct control.'
      : 'Playback is available; use Next, Previous, or Reset for direct control.';
  });
}
applyMotionPreference();
if (motionPreference && motionPreference.addEventListener) motionPreference.addEventListener('change', applyMotionPreference);
function trace(block, action, selectedState) {
  const states = [...block.querySelectorAll('[data-trace-state]')];
  if (!states.length) return;
  let current = states.findIndex(state => !state.hidden);
  if (current < 0) current = 0;
  if (action === 'reset') current = 0;
  if (action === 'previous') current = Math.max(current - 1, 0);
  if (action === 'step') current = Math.min(current + 1, states.length - 1);
  if (action === 'select' && Number.isInteger(selectedState)) current = Math.min(Math.max(selectedState, 0), states.length - 1);
  states.forEach((state, index) => { state.hidden = index !== current; });
  block.querySelectorAll('[data-trace-choice]').forEach(choice => { choice.checked = Number(choice.value) === current; });
  const label = block.querySelector('[data-current-state]');
  if (label) label.textContent = `${current + 1} of ${states.length}`;
  return current < states.length - 1;
}
function pause(index) { if (timers.has(index)) { clearInterval(timers.get(index)); timers.delete(index); } }
document.querySelectorAll('.block-choice').forEach(button => button.addEventListener('click', () => {
  const index = button.dataset.block;
  [...timers.keys()].forEach(pause);
  document.querySelectorAll('.block-choice').forEach(choice => choice.setAttribute('aria-pressed', String(choice === button)));
  document.querySelectorAll('[data-study-block]').forEach(block => {
    const selected = block.dataset.studyBlock === index;
    block.hidden = !selected;
    if (selected) {
      trace(block, 'reset');
      const heading = block.querySelector('h2');
      if (heading) heading.focus({preventScroll: true});
    }
  });
}));
document.querySelectorAll('[data-trace-action]').forEach(button => button.addEventListener('click', () => {
  const index = button.dataset.trace, block = document.querySelector(`[data-study-block="${index}"]`);
  if (!block) return;
  if (button.dataset.traceAction === 'pause') return pause(index);
  if (button.dataset.traceAction === 'play') {
    if (motionPreference && motionPreference.matches) return;
    pause(index); timers.set(index, setInterval(() => { if (!trace(block, 'step')) pause(index); }, 1200)); return;
  }
  pause(index); trace(block, button.dataset.traceAction);
}));
document.querySelectorAll('[data-trace-choice]').forEach(choice => choice.addEventListener('change', () => {
  const index = choice.dataset.traceChoice, block = document.querySelector(`[data-study-block="${index}"]`);
  if (!block || !choice.checked) return;
  pause(index); trace(block, 'select', Number(choice.value));
}));
})();</script>'''


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
        content = f'{problem.get("statement_html") or ""}<section><h2>Examples</h2>{example_blocks or "<p>No structured examples could be extracted; see statement above.</p>"}</section>{_render_runner(problem)}'
    body = f'<h1>{html.escape(title)}</h1><p class="meta">{html.escape(problem.get("difficulty") or "Unknown")} · {"Premium" if problem.get("paid_only") else "Public"}</p><div class="tags">{tags}</div>{content}'
    path.write_text(_page(title, body, home="../index.html"), encoding="utf-8")


def _parse_json(value: Any) -> Any | None:
    try:
        return json.loads(str(value).strip())
    except (TypeError, ValueError):
        return None


def _runner_spec(problem: dict[str, Any]) -> dict[str, Any] | None:
    metadata = _parse_json(problem.get("metadata"))
    if not isinstance(metadata, dict) or not isinstance(metadata.get("name"), str):
        return None
    params = metadata.get("params")
    if not isinstance(params, list) or not problem.get("python_starter"):
        return None
    sample_values = [_parse_json(value) for value in str(problem.get("sample_test_case") or "").splitlines()]
    args = sample_values if len(sample_values) == len(params) and all(value is not None for value in sample_values) else None
    cases = []
    if args is not None:
        for example in problem.get("examples") or []:
            expected = _parse_json(example.get("output"))
            if expected is not None:
                cases.append({"args": args, "expected": expected})
                break
    return {"method": metadata["name"], "params": params, "cases": cases}


def _render_runner(problem: dict[str, Any]) -> str:
    spec = _runner_spec(problem)
    if spec is None:
        return '<section><h2>Local runner</h2><p class="meta">This record has no compatible Python starter and callable metadata.</p></section>'
    code = html.escape(str(problem["python_starter"]))
    cases = html.escape(json.dumps(spec["cases"], ensure_ascii=False, indent=2))
    method, params = html.escape(spec["method"]), html.escape(json.dumps(spec["params"], ensure_ascii=False))
    hint = "An example was prefilled." if spec["cases"] else "Add JSON cases: [{\"args\": [...], \"expected\": ...}]."
    return f'''<section data-runner data-method="{method}" data-params="{params}">
<h2>Local runner</h2><p class="meta">LeetCode-shaped local check: fresh <code>Solution</code> instance per case, exact JSON comparison, and aggregate call time. {hint} Start it with <code>dsa-study serve</code>; opening this file directly cannot execute Python.</p>
<label for="solution-code">Python solution</label><textarea id="solution-code" spellcheck="false">{code}</textarea>
<label for="runner-cases">Test cases (JSON)</label><textarea id="runner-cases" spellcheck="false">{cases}</textarea>
<button type="button" data-run>Run local checks</button><output data-result aria-live="polite">Ready. Code and cases are sent only to your loopback local server and are not saved.</output></section>{_runner_script()}'''


def _runner_script() -> str:
    return '''<script>(() => { const runner = document.querySelector('[data-runner]'); if (!runner) return;
const result = runner.querySelector('[data-result]');
runner.querySelector('[data-run]').addEventListener('click', async () => {
  let cases; try { cases = JSON.parse(runner.querySelector('#runner-cases').value); } catch (error) { result.textContent = `Invalid cases JSON: ${error.message}`; return; }
  result.textContent = 'Running locally…';
  try { const response = await fetch('/api/run', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({code: runner.querySelector('#solution-code').value, method: runner.dataset.method, params: JSON.parse(runner.dataset.params), cases})});
    const report = await response.json(); const runtime = report.runtime_ns == null ? '' : `\\nAggregate call time: ${(report.runtime_ns / 1e6).toFixed(3)} ms`;
    const summary = `${report.status.replaceAll('_', ' ')} — ${report.cases_passed ?? 0}/${report.cases_total ?? cases.length} cases${runtime}`;
    const detail = report.results?.find(item => !item.passed); result.textContent = summary + (detail ? `\\nCase ${detail.index}: expected ${JSON.stringify(detail.expected)}, got ${JSON.stringify(detail.actual)}` : '') + (report.message ? `\\n${report.message}` : '');
  } catch (error) { result.textContent = `Runner unavailable: ${error.message}. Start with dsa-study serve.`; }
}); })();</script>'''
