from pathlib import Path

from dsa_study.catalog import build_topics, sync
from dsa_study.storage import catalog_path, read_json


class FakeClient:
    def catalog_page(self, skip: int, limit: int):
        pages = [
            [{"questionFrontendId": "1", "titleSlug": "two-sum", "title": "Two Sum", "paidOnly": False, "difficulty": "Easy", "acRate": 50, "topicTags": [{"name": "Array", "slug": "array"}, {"name": "Hash Table", "slug": "hash-table"}]}],
            [{"questionFrontendId": "2", "titleSlug": "locked", "title": "Locked", "paidOnly": True, "difficulty": "Hard", "acRate": 1, "topicTags": [{"name": "Array", "slug": "array"}]}],
        ]
        page = pages[skip // limit]
        return page, skip == 0, 2

    def detail(self, slug: str):
        assert slug == "two-sum"
        return {"content": "<p><strong>Input:</strong> nums=[2,7]<br><strong>Output:</strong> [0,1]</p>", "sampleTestCase": "[2,7]\\n9", "hints": [], "metaData": "{}", "codeSnippets": [{"langSlug": "python3", "code": "class Solution:\n    pass"}]}


def test_sync_builds_topic_registry_and_marks_public_lock(tmp_path: Path):
    document = sync(tmp_path, FakeClient(), page_size=1)
    assert [topic["slug"] for topic in document["topics"]] == ["array", "hash-table"]
    assert document["problems"][0]["detail_status"] == "available"
    assert document["problems"][1]["detail_reason"] == "paid_only_public_sync"
    assert read_json(catalog_path(tmp_path), {})["problems"][0]["examples"][0]["output"] == "[0,1]"


def test_topics_are_sorted_and_counted():
    topics = build_topics([{"topics": [{"slug": "tree", "name": "Tree"}, {"slug": "tree", "name": "Tree"}]}, {"topics": [{"slug": "tree", "name": "Tree"}]}])
    assert topics == [{"slug": "tree", "name": "Tree", "problem_count": 2}]


def test_sync_scrubs_retained_detail_when_a_problem_is_paid_only(tmp_path: Path):
    existing = {
        "problems": [{
            "slug": "locked", "id": "2", "detail_status": "available",
            "statement_html": "<p>Old statement</p>", "examples": [{"input": "x", "output": "y"}],
            "python_starter": "class Solution: pass",
        }]
    }
    from dsa_study.storage import write_json
    write_json(catalog_path(tmp_path), existing)

    document = sync(tmp_path, FakeClient(), resume=True, page_size=1)

    locked = document["problems"][1]
    assert locked["detail_status"] == "unavailable"
    assert locked["detail_reason"] == "paid_only_public_sync"
    assert "statement_html" not in locked
    assert "examples" not in locked
    assert "python_starter" not in locked
