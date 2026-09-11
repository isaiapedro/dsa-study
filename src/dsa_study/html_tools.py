"""Safe statement rendering and best-effort example extraction."""

from __future__ import annotations

import html
import re
from html.parser import HTMLParser


ALLOWED_TAGS = {
    "a", "b", "blockquote", "br", "code", "em", "h1", "h2", "h3", "h4", "hr",
    "i", "li", "ol", "p", "pre", "span", "strong", "sub", "sup", "table", "tbody",
    "td", "th", "thead", "tr", "ul",
}
BLOCKED_TAGS = {"iframe", "object", "script", "style", "svg"}


class _Sanitizer(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.blocked_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in BLOCKED_TAGS:
            self.blocked_depth += 1
            return
        if self.blocked_depth:
            return
        if tag not in ALLOWED_TAGS:
            return
        safe_attrs: list[str] = []
        if tag == "a":
            href = dict(attrs).get("href", "") or ""
            if href.startswith(("https://leetcode.com/", "https://leetcode.cn/", "/")):
                safe_attrs.append(f' href="{html.escape(href, quote=True)}"')
        self.parts.append(f"<{tag}{''.join(safe_attrs)}>")

    def handle_endtag(self, tag: str) -> None:
        if tag in BLOCKED_TAGS:
            self.blocked_depth = max(0, self.blocked_depth - 1)
            return
        if self.blocked_depth:
            return
        if tag in ALLOWED_TAGS:
            self.parts.append(f"</{tag}>")

    def handle_data(self, data: str) -> None:
        if self.blocked_depth:
            return
        self.parts.append(html.escape(data))


def sanitize_statement(markup: str) -> str:
    parser = _Sanitizer()
    parser.feed(markup or "")
    parser.close()
    return "".join(parser.parts)


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def text(self) -> str:
        return re.sub(r"[ \t]+", " ", "".join(self.parts).replace("\xa0", " "))


def extract_examples(markup: str) -> list[dict[str, str]]:
    """Extract common rendered examples without claiming a universal LC schema."""
    parser = _TextExtractor()
    parser.feed(markup or "")
    text = parser.text()
    pattern = re.compile(
        r"Input:\s*(?P<input>.*?)\s*Output:\s*(?P<output>.*?)(?=\s*(?:Explanation|Input|Constraints):|$)",
        re.IGNORECASE | re.DOTALL,
    )
    return [
        {"input": match.group("input").strip(), "output": match.group("output").strip()}
        for match in pattern.finditer(text)
        if match.group("input").strip() or match.group("output").strip()
    ]
