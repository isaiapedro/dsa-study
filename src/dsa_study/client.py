"""Thin, isolated client for LeetCode's public web GraphQL surface."""

from __future__ import annotations

import json
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ENDPOINT = "https://leetcode.com/graphql/"
CATALOG_QUERY = """
query problemsetQuestionListV2($filters: QuestionFilterInput, $limit: Int, $searchKeyword: String, $skip: Int, $sortBy: QuestionSortByInput, $categorySlug: String) {
  problemsetQuestionListV2(filters: $filters, limit: $limit, searchKeyword: $searchKeyword, skip: $skip, sortBy: $sortBy, categorySlug: $categorySlug) {
    questions { id titleSlug title questionFrontendId paidOnly difficulty acRate topicTags { name slug } }
    totalLength hasMore
  }
}
"""
CATALOG_FILTERS = {
    "filterCombineType": "ALL",
    "statusFilter": {"questionStatuses": [], "operator": "IS"},
    "difficultyFilter": {"difficulties": [], "operator": "IS"},
    "languageFilter": {"languageSlugs": [], "operator": "IS"},
    "topicFilter": {"topicSlugs": [], "operator": "IS"},
    "acceptanceFilter": {},
    "frequencyFilter": {},
    "frontendIdFilter": {},
    "lastSubmittedFilter": {},
    "publishedFilter": {},
    "companyFilter": {"companySlugs": [], "operator": "IS"},
    "positionFilter": {"positionSlugs": [], "operator": "IS"},
    "positionLevelFilter": {"positionLevelSlugs": [], "operator": "IS"},
    "contestPointFilter": {"contestPoints": [], "operator": "IS"},
    "premiumFilter": {"premiumStatus": [], "operator": "IS"},
}
DETAIL_QUERY = """
query questionData($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    questionId questionFrontendId title titleSlug isPaidOnly difficulty content
    sampleTestCase exampleTestcaseList hints metaData
    topicTags { name slug }
    codeSnippets { lang langSlug code }
  }
}
"""


class LeetCodeClient:
    def __init__(self, *, endpoint: str = ENDPOINT, retries: int = 3, delay_seconds: float = 0.6) -> None:
        self.endpoint = endpoint
        self.retries = retries
        self.delay_seconds = delay_seconds

    def _post(self, query: str, variables: dict[str, Any], operation: str) -> dict[str, Any]:
        payload = json.dumps({"query": query, "variables": variables, "operationName": operation}).encode()
        request = Request(self.endpoint, data=payload, headers={
            "Content-Type": "application/json",
            "User-Agent": "dsa-study-catalog/0.1 (+local study workspace)",
        })
        last_error: Exception | None = None
        for attempt in range(self.retries):
            try:
                with urlopen(request, timeout=30) as response:
                    decoded = json.loads(response.read().decode("utf-8"))
                if decoded.get("errors"):
                    raise RuntimeError(str(decoded["errors"]))
                return decoded.get("data") or {}
            except HTTPError as error:
                # GraphQL validation errors are often returned as HTTP 400.
                # Preserve the provider diagnostic rather than hiding it behind
                # urllib's generic exception text.
                diagnostic = error.read().decode("utf-8", errors="replace")[:1_000]
                last_error = RuntimeError(f"HTTP {error.code}: {diagnostic or error.reason}")
                if attempt + 1 < self.retries:
                    time.sleep(self.delay_seconds * (2**attempt))
            except (URLError, TimeoutError, json.JSONDecodeError, RuntimeError) as error:
                last_error = error
                if attempt + 1 < self.retries:
                    time.sleep(self.delay_seconds * (2**attempt))
        raise RuntimeError(f"LeetCode request failed after {self.retries} attempts: {last_error}")

    def catalog_page(self, skip: int, limit: int) -> tuple[list[dict[str, Any]], bool, int]:
        variables = {
            "filters": CATALOG_FILTERS,
            "limit": limit,
            "searchKeyword": "",
            "skip": skip,
            "sortBy": {"sortField": "CUSTOM", "sortOrder": "ASCENDING"},
            "categorySlug": "all-code-essentials",
        }
        data = self._post(CATALOG_QUERY, variables, "problemsetQuestionListV2")
        page = data.get("problemsetQuestionListV2") or {}
        questions = page.get("questions")
        if not isinstance(questions, list):
            raise RuntimeError("Unexpected catalog response: missing question list.")
        return questions, bool(page.get("hasMore")), int(page.get("totalLength") or len(questions))

    def detail(self, slug: str) -> dict[str, Any] | None:
        data = self._post(DETAIL_QUERY, {"titleSlug": slug}, "questionData")
        question = data.get("question")
        return question if isinstance(question, dict) else None
