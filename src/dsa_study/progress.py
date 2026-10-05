"""Private progress history and deterministic review-queue generation."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from dsa_study.storage import progress_path, read_json, write_json


VALID_STATUSES = {"attempted", "solved", "reviewed"}
_BASE_INTERVAL_DAYS = {1: 1, 2: 2, 3: 4, 4: 7, 5: 14}


def _now() -> datetime:
    return datetime.now(UTC)


def _timestamp(value: datetime) -> str:
    return value.astimezone(UTC).isoformat()


def _parse_timestamp(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)


def record_progress(
    root: Path,
    problem_id: str,
    status: str,
    *,
    confidence: int | None = None,
    note: str | None = None,
    recorded_at: datetime | None = None,
) -> dict[str, Any]:
    """Append a private learning event; this data is never part of the catalog."""
    if status not in VALID_STATUSES:
        raise ValueError(f"status must be one of: {', '.join(sorted(VALID_STATUSES))}")
    if confidence is not None and confidence not in _BASE_INTERVAL_DAYS:
        raise ValueError("confidence must be an integer from 1 to 5")
    if not str(problem_id).strip():
        raise ValueError("problem_id is required")

    path = progress_path(root)
    document = read_json(path, {"schema_version": 1, "events": []})
    events = document.setdefault("events", [])
    event = {"problem_id": str(problem_id), "status": status, "recorded_at": _timestamp(recorded_at or _now())}
    if confidence is not None:
        event["confidence"] = confidence
    if note:
        event["note"] = note
    events.append(event)
    write_json(path, document)
    return event


def build_review_queue(root: Path, catalog: dict[str, Any] | None = None, *, now: datetime | None = None) -> list[dict[str, Any]]:
    """Build a transparent starting review schedule from local study events.

    Attempts are due after one day. Completed items use the most recent
    confidence (default 3) and double their base interval for two reviews.
    This is deliberately a small heuristic, not a personalized memory model.
    """
    document = read_json(progress_path(root), {"events": []})
    by_problem: dict[str, list[dict[str, Any]]] = {}
    for event in document.get("events", []):
        if event.get("status") in VALID_STATUSES and event.get("problem_id") and event.get("recorded_at"):
            by_problem.setdefault(str(event["problem_id"]), []).append(event)

    titles = {str(row.get("id")): row.get("title", "") for row in (catalog or {}).get("problems", [])}
    current = now or _now()
    queue: list[dict[str, Any]] = []
    for problem_id, events in by_problem.items():
        events.sort(key=lambda event: _parse_timestamp(event["recorded_at"]))
        latest = events[-1]
        completed = [event for event in events if event["status"] in {"solved", "reviewed"}]
        confidence = next((event["confidence"] for event in reversed(events) if event.get("confidence") in _BASE_INTERVAL_DAYS), 3)
        interval_days = 1 if latest["status"] == "attempted" else min(_BASE_INTERVAL_DAYS[confidence] * (2 ** min(len(completed) - 1, 2)), 60)
        last_practiced = _parse_timestamp(latest["recorded_at"])
        due_at = last_practiced + timedelta(days=interval_days)
        queue.append({"problem_id": problem_id, "title": titles.get(problem_id, ""), "last_status": latest["status"], "confidence": confidence, "last_practiced_at": _timestamp(last_practiced), "due_at": _timestamp(due_at), "due": due_at <= current, "interval_days": interval_days})
    return sorted(queue, key=lambda item: (item["due_at"], item["confidence"], item["problem_id"]))
