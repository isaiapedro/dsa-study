from datetime import UTC, datetime
from pathlib import Path

from dsa_study.progress import build_review_queue, record_progress
from dsa_study.storage import progress_path, read_json


def test_progress_is_private_and_review_queue_uses_confidence(tmp_path: Path):
    event = record_progress(tmp_path, "1", "solved", confidence=2, note="private", recorded_at=datetime(2026, 9, 1, tzinfo=UTC))
    assert event["note"] == "private"
    assert progress_path(tmp_path) == tmp_path / ".dsa-study" / "progress.json"
    assert read_json(progress_path(tmp_path), {})["events"][0]["problem_id"] == "1"
    queue = build_review_queue(tmp_path, {"problems": [{"id": "1", "title": "Two Sum"}]}, now=datetime(2026, 9, 3, tzinfo=UTC))
    assert queue[0]["title"] == "Two Sum"
    assert queue[0]["interval_days"] == 2
    assert queue[0]["due"] is True


def test_attempt_is_due_next_day_and_completed_reviews_expand_interval(tmp_path: Path):
    record_progress(tmp_path, "7", "attempted", recorded_at=datetime(2026, 9, 1, tzinfo=UTC))
    assert build_review_queue(tmp_path, now=datetime(2026, 9, 2, tzinfo=UTC))[0]["due"] is True
    record_progress(tmp_path, "7", "solved", confidence=3, recorded_at=datetime(2026, 9, 2, tzinfo=UTC))
    record_progress(tmp_path, "7", "reviewed", confidence=3, recorded_at=datetime(2026, 9, 6, tzinfo=UTC))
    queue = build_review_queue(tmp_path, now=datetime(2026, 9, 13, tzinfo=UTC))
    assert queue[0]["interval_days"] == 8
    assert queue[0]["due"] is False
