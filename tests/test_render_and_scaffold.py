from pathlib import Path

from dsa_study.render import render_site
from dsa_study.scaffold import create_solution
from dsa_study.storage import catalog_path, write_json


def test_render_writes_topic_and_problem_pages(tmp_path: Path):
    document = {"synced_at": "now", "topics": [{"slug": "array", "name": "Array", "problem_count": 1}], "problems": [{"id": "1", "slug": "two-sum", "title": "Two Sum", "difficulty": "Easy", "paid_only": False, "topics": [{"slug": "array", "name": "Array"}], "detail_status": "available", "statement_html": "<p>Find it.</p>", "examples": [{"input": "a", "output": "b"}]}]}
    render_site(document, tmp_path / "site")
    assert "Array (1)" in (tmp_path / "site" / "index.html").read_text()
    detail = (tmp_path / "site" / "problems" / "two-sum.html").read_text()
    assert "Example 1" in detail
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
