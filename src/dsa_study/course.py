"""Original textbook-style lessons, independent of imported and private data."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

from dsa_study.textbook_pages import references_for


COURSE_ROOT = Path(__file__).resolve().parents[2] / "learning_blocks"


def load_course(root: Path = COURSE_ROOT) -> list[dict]:
    modules = json.loads((root / "course.json").read_text(encoding="utf-8"))["modules"]
    identifiers = set()
    for index, module in enumerate(modules, 1):
        identifier = module["id"]
        if not re.fullmatch(r"[0-9]{2}-[a-z-]+", identifier) or identifier in identifiers:
            raise ValueError("Invalid or duplicate course module identifier")
        if module["file"] != identifier + ".md" or module["sequence"] != index:
            raise ValueError("Course files and sequence must match their module identifiers")
        identifiers.add(identifier)
        module["body"] = (root / module["file"]).read_text(encoding="utf-8")
    return modules


def _inline(text: str) -> str:
    """Render links and inline code, escaping all other source text."""
    tokens = re.compile(r"`([^`]+)`|\[([^\]]+)\]\(([^\s)]+)\)")
    result, start = [], 0
    for match in tokens.finditer(text):
        result.append(html.escape(text[start:match.start()]))
        code, label, target = match.groups()
        if code is not None:
            result.append(f"<code>{html.escape(code)}</code>")
        elif urlsplit(target).scheme == "https" and urlsplit(target).netloc:
            result.append(f'<a href="{html.escape(target, quote=True)}">{html.escape(label)}</a>')
        else:
            result.append(html.escape(label))
        start = match.end()
    result.append(html.escape(text[start:]))
    return "".join(result)


def render_lesson(body: str, module_id: str = "") -> str:
    """Render the deliberately small authored Markdown format without raw HTML."""
    result, paragraph = [], []

    def flush() -> None:
        if paragraph:
            text = " ".join(paragraph)
            if text.startswith("Practice:"):
                result.append('<details><summary>Plan your solution</summary><p>What is given and what must you return? Which input limit matters? What information will you keep between steps? Why does this method fit?</p></details>')
            completion = re.match(r"(Try this: .+?[.?])\s+(.+)", text)
            if completion and not re.match(r"(?:Then|Explain|Which|Why|What|Complete|Predict|Compare|Use|Check|Keep|Decide|Count|Identify|Compute|List|Trace|Write|Separate|Repeat|Revisit)\b", completion[2]):
                result.append(f'<p>{_inline(completion[1])}</p><details><summary>Hint and check</summary><p>{_inline(completion[2])}</p></details>')
            else:
                result.append(f"<p>{_inline(text)}</p>")
            paragraph.clear()

    for line in body.splitlines():
        heading = re.fullmatch(r"(#{1,3}) (.+)", line)
        if heading:
            flush()
            level, title = len(heading[1]), heading[2]
            anchor = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
            result.append(f'<h{level} id="{anchor}">{html.escape(title)}</h{level}>')
            section = re.match(r"(\d+\.\d+)\b", title)
            references = references_for(module_id, section[1]) if level == 2 and section else ()
            if references:
                links = " · ".join(
                    f'<a href="{html.escape(url, quote=True)}">{html.escape(label)}</a>'
                    for label, url in references
                )
                result.append(f'<p class="textbook-pages"><strong>Textbook pages:</strong> {links}</p>')
        elif not line.strip():
            flush()
        else:
            paragraph.append(line.strip())
    flush()
    return "\n".join(result)


def course_index(modules: list[dict]) -> str:
    items = "".join(f'<li><a href="course/{m["id"]}.html">{m["sequence"]}. {html.escape(m["title"])}</a></li>' for m in modules)
    return f'''<section aria-labelledby="course-heading"><h1 id="course-heading">Data structures and algorithms</h1>
<p>Read one section at a time. Follow its example, predict the missing step, then try the linked problems. Explain your answer and check an edge case. In a later session, recall the idea before reopening the lesson.</p>
<details><summary>A 45-minute study session</summary><p>Recall an earlier idea for 3 minutes; read for 7; trace an example for 7; complete a missing step for 8; compare methods for 4; attempt a problem for 10; check and correct your reasoning for 6. Keep tool use within 8 minutes. A module can take several sessions.</p></details>
<nav aria-label="Course modules"><ol style="list-style:none;padding-left:0">{items}</ol></nav>
<p><a href="course/references.html">Textbooks and learning references</a> · <a href="#study-heading">Interactive examples</a></p></section>'''


def render_course(destination: Path, page) -> str:
    modules = load_course()
    output = destination / "course"
    output.mkdir(exist_ok=True)
    for index, module in enumerate(modules):
        neighbors = []
        if index:
            previous = modules[index - 1]
            neighbors.append(f'<a href="{previous["id"]}.html">Previous: {html.escape(previous["title"])}</a>')
        if index + 1 < len(modules):
            following = modules[index + 1]
            neighbors.append(f'<a href="{following["id"]}.html">Next: {html.escape(following["title"])}</a>')
        headings = re.findall(r"^## (.+)$", module["body"], re.MULTILINE)
        contents = "".join(f'<li><a href="#{re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")}">{html.escape(title)}</a></li>' for title in headings)
        references = []
        if module["clrs"]:
            references.append("CLRS chapters/appendices " + ", ".join(module["clrs"]))
        if module["sedgewick"]:
            references.append("Sedgewick/Wayne sections " + ", ".join(module["sedgewick"]))
        body = f'<nav aria-label="In this module"><ul>{contents}</ul></nav><main class="lesson">{render_lesson(module["body"], module["id"])}</main><p class="meta">Further reading: {html.escape("; ".join(references))}. <a href="references.html">References</a></p><nav aria-label="Adjacent modules">{" · ".join(neighbors)}</nav>'
        (output / (module["id"] + ".html")).write_text(page(module["title"], body, home="../index.html"), encoding="utf-8")
    references = '''<main><h1>Textbooks and learning references</h1>
<p><a href="https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/">Introduction to Algorithms, fourth edition</a>, by Cormen, Leiserson, Rivest, and Stein, guides the theory and breadth. <a href="https://algs4.cs.princeton.edu/home/">Algorithms, fourth edition</a>, by Sedgewick and Wayne, guides representations, traces, and applications. The course spans their chapter topics in original introductory explanations; consult the books for full proofs, implementation details, and exercises.</p>
<p>Every numbered lesson section includes direct page links to the relevant edition in Google Books. The links use exact printed page numbers; limited preview access is controlled by the rights holder. The local Technology Knowledge wiki supplies the governed textbook records and bounded references on hashing, amortized analysis, and string matching. The course chapter map and exact local source paths are recorded in CURRICULUM.md and ACADEMIC_REFERENCE_GUIDELINES.md in the project.</p>
<p>Worked examples, completion exercises, feedback, later recall, and comparisons between related techniques follow the project's learning guidelines and Planning Science wiki. These evidence-informed choices do not establish a guaranteed learning outcome or a universal review interval.</p>
<p>Each numbered section has LeetCode practice. Related exercises are labeled where they cover only part of a topic; local exercises cover the missing operation. Some linked problems require a subscription. Problem availability follows the provider; the original lessons remain readable offline.</p></main>'''
    (output / "references.html").write_text(page("References", references, home="../index.html"), encoding="utf-8")
    return course_index(modules)
