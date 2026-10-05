"""Read project-authored DSA learning-block source without learner state."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


_BLOCKS_PATH = Path(__file__).resolve().parents[2] / "learning_blocks" / "blocks.json"


# These are project-authored routing rules, not a recommendation engine.  They
# make the catalog connection inspectable and keep it independent of progress,
# answers, or any inferred learner profile.  Catalog metadata has topic tags,
# but not reliable machine-readable constraints, so constraints explain the
# intended use of a selected problem instead of pretending to filter on fields
# that do not exist.
_PRACTICE_MAPPINGS: dict[str, dict[str, Any]] = {
    "arrays-indexing-contracts": {
        "technique": "single-pass indexed scan",
        "required_topic_slugs": ["array"],
        "preferred_topic_slugs": [],
        "constraints": [
            "the input has stable indexed positions",
            "the task can be solved by one bounded left-to-right pass",
            "the response needs a position, value, or absence result",
        ],
    },
    "hashing-collision-reasoning": {
        "technique": "key-to-value lookup with equality checks",
        "required_topic_slugs": ["hash-table"],
        "preferred_topic_slugs": ["array"],
        "constraints": [
            "lookup is by key identity rather than sorted order",
            "extra space for stored keys is acceptable",
            "the explanation qualifies expected and worst-case cost",
        ],
    },
    "two-pointers-monotonic-movement": {
        "technique": "two-pointer monotone search",
        "required_topic_slugs": ["array"],
        "preferred_topic_slugs": ["two-pointers"],
        "constraints": [
            "the data is ordered or can be ordered without violating the task",
            "a comparison justifies discarding a boundary monotonically",
            "linear auxiliary space is undesirable or ordering is otherwise useful",
        ],
    },
    "binary-search-interval-invariant": {
        "technique": "binary search over a monotone interval",
        "required_topic_slugs": ["binary-search"],
        "preferred_topic_slugs": ["array"],
        "constraints": [
            "the input is ordered under the comparison used",
            "random indexing makes midpoint selection direct",
            "each comparison proves one interval can be discarded",
        ],
    },
    "linked-lists-rewiring-contracts": {
        "technique": "local linked-list pointer rewiring",
        "required_topic_slugs": ["linked-list"],
        "preferred_topic_slugs": [],
        "constraints": [
            "the operation changes links rather than indexed positions",
            "every retained node must remain reachable after each assignment",
            "the head and terminal-node cases need explicit handling",
        ],
    },
    "stacks-queues-order-contracts": {
        "technique": "stack or queue work-order selection",
        "required_topic_slugs": ["stack"],
        "preferred_topic_slugs": ["queue"],
        "constraints": [
            "the task's next-item policy is last-in-first-out or first-in-first-out",
            "push/enqueue and pop/dequeue state is represented explicitly",
            "empty-structure behavior is defined before removal",
        ],
    },
    "trees-recursive-return-contracts": {
        "technique": "recursive subtree-return reasoning",
        "required_topic_slugs": ["binary-tree"],
        "preferred_topic_slugs": ["tree", "recursion"],
        "constraints": [
            "each call has a defined subtree input and return value",
            "base cases make absent children explicit",
            "the parent combines child returns without assuming global order",
        ],
    },
    "bfs-dfs-frontier-visited-contracts": {
        "technique": "frontier traversal with visited-state discipline",
        "required_topic_slugs": ["breadth-first-search"],
        "preferred_topic_slugs": ["graph", "depth-first-search"],
        "constraints": [
            "the graph representation makes neighbors available",
            "visited state prevents duplicate expansion or cycles",
            "the traversal order is justified by the question being answered",
        ],
    },
    "dynamic-programming-dependency-contracts": {
        "technique": "dynamic-programming state and dependency transition",
        "required_topic_slugs": ["dynamic-programming"],
        "preferred_topic_slugs": ["memoization"],
        "constraints": [
            "the state contains enough information for the remaining subproblem",
            "base cases and dependency order are explicit",
            "the transition does not depend on discarded history",
        ],
    },
}


_INTERVIEW_PROMPTS = (
    ("Approach", "State the approach and why {technique} fits this input."),
    ("Correctness", "Name the invariant or discard argument that makes the approach correct."),
    ("Complexity", "Claim time and auxiliary-space cost, including any required assumption."),
    ("Boundary test", "Give an edge case and state the expected result before running code."),
    ("Contrast", "Name a close alternative and the condition that would make it preferable."),
)


def load_learning_blocks() -> list[dict[str, Any]]:
    """Return validated, tracked authored blocks in their declared sequence."""
    payload = json.loads(_BLOCKS_PATH.read_text(encoding="utf-8"))
    blocks = sorted(payload["blocks"], key=lambda block: block["sequence"])
    for block in blocks:
        # The tracked source stays focused on a block's lesson.  Attach the
        # shared, code-competition practice contract at load time so both the
        # schema and renderer use one reviewable source of truth.
        mapping = _PRACTICE_MAPPINGS.get(block.get("id", ""))
        if mapping is not None:
            block["catalog_practice"] = mapping
            block["interview_prompts"] = interview_prompts(mapping["technique"])
        validate_learning_block(block)
    return blocks


def interview_prompts(technique: str) -> list[dict[str, str]]:
    """Return reusable, in-memory prompts for a single practice attempt."""
    return [
        {"label": label, "prompt": prompt.format(technique=technique)}
        for label, prompt in _INTERVIEW_PROMPTS
    ]


def select_catalog_practice(block: dict[str, Any], problems: list[dict[str, Any]], *, limit: int = 5) -> list[dict[str, Any]]:
    """Select explainable catalog practice using declared tag rules only.

    Preferred tags rank focused candidates first; required tags remain the
    stable eligibility rule.  No learner state participates in selection.
    """
    mapping = block.get("catalog_practice") or {}
    required = set(mapping.get("required_topic_slugs") or [])
    preferred = set(mapping.get("preferred_topic_slugs") or [])
    if not required or limit < 1:
        return []

    eligible = []
    for problem in problems:
        topic_slugs = {str(topic.get("slug")) for topic in problem.get("topics") or [] if isinstance(topic, dict)}
        if required <= topic_slugs:
            eligible.append((bool(preferred & topic_slugs), problem))
    eligible.sort(key=lambda item: (not item[0], _problem_sort_key(item[1])))
    return [problem for _, problem in eligible[:limit]]


def _problem_sort_key(problem: dict[str, Any]) -> tuple[int, str]:
    identifier = str(problem.get("id", ""))
    return (int(identifier) if identifier.isdigit() else 10**9, str(problem.get("slug", "")))


_QUESTION_KINDS = {"retrieval", "invariant", "next-state", "contrast", "invalid-use"}
_PRE_CODE_LENSES = {"input_output", "constraint", "state_invariant", "selection"}


def validate_learning_block(block: dict[str, Any]) -> None:
    """Reject incomplete instructional material before it reaches the renderer.

    These checks deliberately concern authored pedagogy, never learner answers or
    progress.  A block is a concise, reviewable teaching unit rather than an
    unconstrained content feed.
    """
    identifier = block.get("id", "<unknown>")
    if block.get("duration_minutes") != 45 or block.get("tool_time_ceiling_minutes") != 8:
        raise ValueError(f"{identifier}: blocks must be 45 minutes with an 8-minute tool ceiling")
    if set((block.get("outcomes") or {})) != {"foundation", "interview", "professional_transfer"}:
        raise ValueError(f"{identifier}: missing required outcomes")
    questions = block.get("questions") or []
    if len(questions) != 5 or {question.get("kind") for question in questions} != _QUESTION_KINDS:
        raise ValueError(f"{identifier}: require one authored question of each required kind")
    if block.get("question_provenance") != "project-authored-review-required":
        raise ValueError(f"{identifier}: questions must remain authored and review-required")
    checkpoint = block.get("pre_code_checkpoint") or {}
    prompts = checkpoint.get("prompts") or []
    if {prompt.get("lens") for prompt in prompts} != _PRE_CODE_LENSES:
        raise ValueError(f"{identifier}: pre-code checkpoint needs all four reasoning lenses")
    context = block.get("curriculum_context") or {}
    if not isinstance(context.get("part_of"), str) or not context.get("selection_dimensions"):
        raise ValueError(f"{identifier}: curriculum context must expose a part-of path and selection dimensions")
    practice = block.get("catalog_practice") or {}
    if not isinstance(practice.get("technique"), str) or not practice.get("required_topic_slugs") or not practice.get("constraints"):
        raise ValueError(f"{identifier}: catalog practice needs technique, required topic tags, and constraints")
    prompts = block.get("interview_prompts") or []
    if len(prompts) != len(_INTERVIEW_PROMPTS) or any(not prompt.get("label") or not prompt.get("prompt") for prompt in prompts):
        raise ValueError(f"{identifier}: catalog practice needs reusable interview prompts")
