"""Catalog normalization, resumable synchronization, and canonical topic registry."""

from __future__ import annotations

from datetime import UTC, datetime
import json
from pathlib import Path
from typing import Any

from dsa_study.client import LeetCodeClient
from dsa_study.html_tools import extract_examples, sanitize_statement
from dsa_study.storage import catalog_path, checkpoint_path, read_json, write_json


DETAIL_FIELDS = {
    "statement_html",
    "examples",
    "sample_test_case",
    "hints",
    "metadata",
    "python_starter",
}


def _now() -> str:
    return datetime.now(UTC).isoformat()


def normalize_catalog_question(question: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": str(question.get("questionFrontendId") or question.get("id") or ""),
        "slug": str(question.get("titleSlug") or ""),
        "title": str(question.get("title") or ""),
        "difficulty": str(question.get("difficulty") or "Unknown"),
        "paid_only": bool(question.get("paidOnly")),
        "acceptance_rate": question.get("acRate"),
        "topics": sorted(
            [{"slug": str(tag.get("slug") or ""), "name": str(tag.get("name") or "")} for tag in question.get("topicTags") or []],
            key=lambda tag: tag["slug"],
        ),
        "detail_status": "pending",
    }


def build_topics(problems: list[dict[str, Any]]) -> list[dict[str, Any]]:
    registry: dict[str, dict[str, Any]] = {}
    for problem in problems:
        seen_slugs: set[str] = set()
        for topic in problem.get("topics") or []:
            slug = topic.get("slug") or ""
            if not slug or slug in seen_slugs:
                continue
            seen_slugs.add(slug)
            entry = registry.setdefault(slug, {"slug": slug, "name": topic.get("name") or slug, "problem_count": 0})
            entry["problem_count"] += 1
    return sorted(registry.values(), key=lambda item: (item["name"].casefold(), item["slug"]))


def audit_catalog(document: dict[str, Any]) -> dict[str, int]:
    """Return coverage counts without copying provider content into source records."""
    problems = document.get("problems") or []
    available = [row for row in problems if row.get("detail_status") == "available"]
    compatible = 0
    for row in available:
        try:
            metadata = json.loads(row.get("metadata") or "{}")
        except (TypeError, ValueError):
            metadata = {}
        compatible += bool(row.get("python_starter") and isinstance(metadata.get("name"), str) and isinstance(metadata.get("params"), list))
    return {
        "problems": len(problems), "public_details": len(available),
        "paid_or_unavailable": len(problems) - len(available),
        "missing_topics": sum(not row.get("topics") for row in problems),
        "missing_examples": sum(not row.get("examples") for row in available),
        "missing_python_starter": sum(not row.get("python_starter") for row in available),
        "runner_compatible": compatible,
    }


def repair_examples(document: dict[str, Any]) -> int:
    """Re-extract local generated examples after an extractor improvement.

    This never fetches a provider response. It only derives fresh structured
    fields from the already ignored local statement markup.
    """
    repaired = 0
    for row in document.get("problems") or []:
        markup = row.get("statement_html")
        if not markup:
            continue
        examples = extract_examples(markup)
        if examples and examples != row.get("examples"):
            row["examples"] = examples
            repaired += 1
    return repaired


def sync(root: Path, client: LeetCodeClient, *, resume: bool = False, page_size: int = 100) -> dict[str, Any]:
    if page_size < 1:
        raise ValueError("page_size must be greater than zero")

    existing = read_json(catalog_path(root), {}) if resume else {}
    existing_by_slug = {row["slug"]: row for row in existing.get("problems", []) if row.get("slug")}
    catalog_rows: list[dict[str, Any]] = []
    skip = 0
    while True:
        page, has_more, _total = client.catalog_page(skip, page_size)
        catalog_rows.extend(normalize_catalog_question(question) for question in page)
        if not has_more:
            break
        skip += len(page)
        if not page:
            raise RuntimeError("Catalog reported more pages but returned no questions.")

    problems: list[dict[str, Any]] = []
    seen_problem_slugs: set[str] = set()
    for row in catalog_rows:
        slug = row["slug"]
        if not slug:
            # A detail query cannot be made without a stable title slug. Keep
            # the metadata visible but make its unavailable state explicit.
            row["detail_status"] = "unavailable"
            row["detail_reason"] = "missing_title_slug"
        elif slug in seen_problem_slugs:
            # Do not fetch or render an ambiguous duplicate remote identifier.
            # The provider catalogue should have unique slugs, so fail early
            # rather than writing an output page over another problem's page.
            raise RuntimeError(f"Unexpected catalog response: duplicate title slug {slug!r}.")
        seen_problem_slugs.add(slug)
        old = existing_by_slug.get(row["slug"], {})
        if old.get("detail_status") in {"available", "unavailable"}:
            row.update({key: old[key] for key in DETAIL_FIELDS | {"detail_status", "detail_reason"} if key in old})
        if row.get("paid_only"):
            _mark_unavailable(row, "paid_only_public_sync")
        problems.append(row)
    document = {"synced_at": _now(), "source": "leetcode-public-graphql", "problems": problems, "topics": build_topics(problems)}
    write_json(catalog_path(root), document)

    checkpoint = read_json(checkpoint_path(root), {"completed_slugs": []}) if resume else {"completed_slugs": []}
    completed = set(checkpoint.get("completed_slugs") or [])
    for row in problems:
        slug = row["slug"]
        if not slug or slug in completed or row.get("paid_only"):
            continue
        try:
            detail = client.detail(slug)
            if not detail or not detail.get("content"):
                _mark_unavailable(row, "not_publicly_readable")
            else:
                markup = str(detail["content"])
                row.update({
                    "detail_status": "available",
                    "statement_html": sanitize_statement(markup),
                    "examples": extract_examples(markup),
                    "sample_test_case": detail.get("sampleTestCase") or "",
                    "hints": detail.get("hints") or [],
                    "metadata": detail.get("metaData") or "",
                    "python_starter": next((snippet.get("code", "") for snippet in detail.get("codeSnippets") or [] if snippet.get("langSlug") == "python3"), ""),
                })
                row.pop("detail_reason", None)
        except RuntimeError as error:
            row["detail_status"] = "error"
            row["detail_reason"] = str(error)
        # Failed requests deliberately remain outside the checkpoint so a later
        # `sync --resume` retries them instead of preserving a transient error.
        if row.get("detail_status") != "error":
            completed.add(slug)
        checkpoint = {"completed_slugs": sorted(completed), "updated_at": _now()}
        write_json(checkpoint_path(root), checkpoint)
        write_json(catalog_path(root), document)
    document["topics"] = build_topics(problems)
    write_json(catalog_path(root), document)
    return document


def _mark_unavailable(row: dict[str, Any], reason: str) -> None:
    """Remove retained provider detail whenever it is no longer readable."""
    for field in DETAIL_FIELDS:
        row.pop(field, None)
    row["detail_status"] = "unavailable"
    row["detail_reason"] = reason
