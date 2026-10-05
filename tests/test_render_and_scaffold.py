from pathlib import Path

from dsa_study.learning_blocks import load_learning_blocks
from dsa_study.render import render_site
from dsa_study.scaffold import create_solution
from dsa_study.storage import catalog_path, write_json


def test_render_writes_topic_and_problem_pages(tmp_path: Path):
    document = {"synced_at": "now", "topics": [{"slug": "array", "name": "Array", "problem_count": 1}], "problems": [{"id": "1", "slug": "two-sum", "title": "Two Sum", "difficulty": "Easy", "paid_only": False, "topics": [{"slug": "array", "name": "Array"}], "detail_status": "available", "statement_html": "<p>Find it.</p>", "examples": [{"input": "a", "output": "[0,1]"}], "sample_test_case": "[2,7,11,15]\n9", "metadata": '{"name":"twoSum","params":[{"name":"nums","type":"integer[]"},{"name":"target","type":"integer"}]}', "python_starter": "class Solution:\n    pass"}]}
    render_site(document, tmp_path / "site")
    assert "Array (1)" in (tmp_path / "site" / "index.html").read_text()
    index = (tmp_path / "site" / "index.html").read_text()
    assert 'id="catalog-toggle"' in index
    assert 'aria-controls="catalog-panel"' in index
    assert 'Show full problem list' in index
    assert 'background:#0b1220' in index
    detail = (tmp_path / "site" / "problems" / "two-sum.html").read_text()
    assert "Example 1" in detail
    assert "Local runner" in detail
    assert "data-run" in detail
    assert 'href="../index.html"' in detail


def test_solution_scaffold_will_not_overwrite(tmp_path: Path):
    (tmp_path / "pyproject.toml").write_text("")
    (tmp_path / "manifest.yaml").write_text("")
    write_json(catalog_path(tmp_path), {"problems": [{"id": "1", "slug": "two-sum", "title": "Two Sum", "difficulty": "Easy", "python_starter": "class Solution:\n    pass"}]})
    target = create_solution(tmp_path, "1")
    assert (target / "solution.py").exists()
    try:
        create_solution(tmp_path, "1")
    except RuntimeError as error:
        assert "Refusing to overwrite" in str(error)
    else:
        raise AssertionError("expected overwrite protection")


def test_render_never_uses_an_untrusted_slug_as_a_path(tmp_path: Path):
    document = {"topics": [], "problems": [{
        "id": "1", "slug": "../../outside", "title": "Unsafe", "difficulty": "Easy",
        "paid_only": False, "topics": [], "detail_status": "unavailable",
    }]}
    render_site(document, tmp_path / "site")
    assert not (tmp_path / "outside.html").exists()
    assert len(list((tmp_path / "site" / "problems").glob("problem-*.html"))) == 1


def test_render_study_block_is_accessible_and_does_not_persist_answers(tmp_path: Path):
    block = {
        "id": "array-contract", "title": "Array contract", "sequence": 1,
        "duration_minutes": 45, "tool_time_ceiling_minutes": 8,
        "target": "Maintain a valid index.", "expected_complexity": "O(n) time; O(1) space.",
        "outcomes": {"foundation": "State the bounds invariant."},
        "theory": "An index is valid only inside the array bounds.",
        "visual": {"kind": "indexed-array-trace", "label": "Indexed array", "prediction_checkpoint": "Will i advance?", "states": [
            {"step": 1, "array": [3, 5], "i": 0, "message": "Inspect index zero."},
            {"step": 2, "array": [3, 5], "i": 2, "message": "Stop before an invalid read."},
        ]},
        "questions": [{"kind": "retrieval", "prompt": f"Prompt {number}", "feedback": "Feedback."} for number in range(1, 6)],
        "pre_code_checkpoint": {"purpose": "Plan first.", "prompts": [
            {"lens": "input_output", "label": "Input/output", "prompt": "What enters and leaves?"},
            {"lens": "constraint", "label": "Constraint", "prompt": "What limits the approach?"},
            {"lens": "state_invariant", "label": "State/invariant", "prompt": "What stays true?"},
            {"lens": "selection", "label": "Selection", "prompt": "Why this technique?"},
        ]},
        "curriculum_context": {"part_of": "Foundations", "prerequisites": [], "selection_dimensions": ["indexed input"]},
        "worked_example": {"model": "Trace one valid index."},
        "faded_scaffold": {"prompt": "Complete the guard."},
        "independent_practice": {"exercise": "Test an empty input."},
        "feedback_checklist": ["State the invariant."], "exit_summary": "Name an invalid use.",
    }
    render_site({"topics": [], "problems": []}, tmp_path / "site", learning_blocks=[block])
    page = (tmp_path / "site" / "index.html").read_text()
    assert page.count('<textarea ') == 9
    assert "Plan your solution" in page
    assert "Related ideas" in page
    assert 'data-trace-action="play"' in page
    assert 'data-trace-action="pause"' in page
    assert 'data-trace-action="previous"' in page
    assert 'data-trace-action="step"' in page
    assert 'data-trace-action="reset"' in page
    assert 'aria-live="polite"' in page
    assert 'tabindex="-1"' in page
    assert 'data-motion-status="0"' in page
    assert "prefers-reduced-motion: reduce" in page
    assert 'data-trace-choice="0"' in page
    assert 'type="radio"' in page
    assert 'name="trace-choice-0"' in page
    assert 'class="array-diagram"' in page
    assert 'class="cell active"' in page
    assert "localStorage" not in page and "sessionStorage" not in page and "fetch(" not in page


def test_render_catalog_practice_exposes_fixed_rules_and_local_interview_prompts(tmp_path: Path):
    block = next(block for block in load_learning_blocks() if block["id"] == "two-pointers-monotonic-movement")
    document = {"topics": [], "problems": [
        {"id": "2", "slug": "two-pointer", "title": "Two-pointer practice", "difficulty": "Easy", "topics": [{"slug": "array", "name": "Array"}, {"slug": "two-pointers", "name": "Two Pointers"}], "detail_status": "unavailable", "paid_only": False},
        {"id": "3", "slug": "array-scan", "title": "Array scan", "difficulty": "Easy", "topics": [{"slug": "array", "name": "Array"}], "detail_status": "unavailable", "paid_only": False},
    ]}

    render_site(document, tmp_path / "site", learning_blocks=[block])
    page = (tmp_path / "site" / "index.html").read_text()

    assert "Focused catalog practice" in page
    assert "Practice <strong>two-pointer monotone search</strong>" in page
    assert "not a learner profile" not in page
    assert page.index("Two-pointer practice") < page.index("Array scan")
    assert "Interview practice prompts" in page
    assert 'name="interview-0-0"' in page
    assert "localStorage" not in page and "sessionStorage" not in page


def test_all_authored_visual_kinds_render_semantic_primitives(tmp_path: Path):
    render_site({"topics": [], "problems": []}, tmp_path / "site", learning_blocks=load_learning_blocks())
    page = (tmp_path / "site" / "index.html").read_text()

    for caption in (
        "Binary-search interval (inclusive bounds)",
        "Linked nodes and next references",
        "Stack state; the top is the removal end",
        "Queue state; front leaves and rear receives",
        "Tree calls and returned values",
        "Graph frontier order",
        "Dynamic-programming states and dependencies",
    ):
        assert caption in page
