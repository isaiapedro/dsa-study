"""Check textbook coverage, practice coverage, and readable offline navigation."""

import re
from pathlib import Path

from dsa_study.course import load_course, render_lesson
from dsa_study.learning_blocks import load_learning_blocks
from dsa_study.render import render_site
from dsa_study.textbook_pages import references_for


def test_course_covers_both_textbook_contents_and_every_section_has_practice():
    modules = load_course()
    assert len(modules) == 20
    assert {chapter for m in modules for chapter in m["clrs"]} == {
        *(str(n) for n in range(1, 36)), "A", "B", "C", "D",
    }
    expected = {f"{chapter}.{section}" for chapter, count in [(1, 5), (2, 5), (3, 5), (4, 4), (5, 5), (6, 6)] for section in range(1, count + 1)}
    assert {section for m in modules for section in m["sedgewick"]} == expected
    for module in modules:
        sections = re.split(r"^## ", module["body"], flags=re.MULTILINE)[1:]
        assert sections
        for section in sections:
            if section.startswith("Review"):
                continue
            assert re.match(r"\d+\.\d+ ", section)
            assert "Try this:" in section
            assert "Practice:" in section
            assert re.search(r"https://leetcode.com/problems/[a-z0-9-]+/", section)
            assert len(section.split()) >= 90
    identifiers = {m["id"] for m in modules}
    assert all(b["course_module"] in identifiers for b in load_learning_blocks())


def test_every_lesson_section_has_an_exact_textbook_page_link():
    for module in load_course():
        for section in re.findall(r"^## (\d+\.\d+) ", module["body"], re.MULTILINE):
            references = tuple(references_for(module["id"], section))
            assert references, f"{module['id']} {section} lacks a page reference"
            for label, url in references:
                assert " p. " in label
                assert re.fullmatch(r"https://books\.google\.com/books\?id=[A-Za-z0-9_-]+&pg=PA\d+", url)


def test_course_pages_work_without_imported_catalog_or_learner_state(tmp_path: Path):
    render_site({"topics": [], "problems": []}, tmp_path)
    index = (tmp_path / "index.html").read_text()
    assert index.index('id="course-heading"') < index.index('id="study-heading"')
    for module in load_course():
        relative = f'course/{module["id"]}.html'
        assert f'href="{relative}"' in index
        page = (tmp_path / relative).read_text()
        assert "Plan your solution" in page
        assert page.count("Textbook pages:") == len(re.findall(r"^## \d+\.\d+ ", module["body"], re.MULTILINE))
        assert "Practice:" in page
        assert 'href="../index.html"' in page
        for target in re.findall(r'href="([^"]+)"', page):
            if target.startswith("https://"):
                continue
            if target.startswith("#"):
                assert f'id="{target[1:]}"' in page
            else:
                assert ((tmp_path / "course") / target).is_file()
        assert "<script" not in page
        assert "localStorage" not in page and "fetch(" not in page
    assert (tmp_path / "course/references.html").is_file()


def test_course_renderer_escapes_markup_and_rejects_active_links():
    page = render_lesson('# Example\n\n<script>alert(1)</script> [bad](javascript:alert) [ok](https://example.org/)\n\n## 1.1 A & B\n\nUse `x < 2`.')
    assert "<script>" not in page
    assert "javascript:" not in page
    assert '<a href="https://example.org/">ok</a>' in page
    assert "<code>x &lt; 2</code>" in page
    assert 'id="1-1-a-b"' in page


def test_completion_feedback_follows_a_prediction_and_build_needs_no_catalog(tmp_path, monkeypatch):
    from dsa_study import cli

    page = render_lesson("Try this: what follows 2, 4? The next value is 6.")
    assert page.index("what follows") < page.index("<details>") < page.index("The next value")
    monkeypatch.setattr(cli, "project_root", lambda: tmp_path)
    cli.main(["build"])
    assert (tmp_path / "site/course/20-hard-problems.html").is_file()
    assert not (tmp_path / "data/catalog.json").exists()
