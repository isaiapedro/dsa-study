"""Opt-in, real-browser checks for the generated learning-block interface.

Set ``DSA_STUDY_BROWSER`` to a Chromium-family executable to run these tests.
Keeping the browser path explicit avoids downloading a browser or adding a
runtime dependency to this local-first project.  The probe is injected only
into a temporary rendered page and never receives learner data.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

from dsa_study.render import render_site


def _browser_blocks() -> list[dict[str, object]]:
    """Small original fixture, isolated from the evolving authored curriculum."""
    def block(title: str) -> dict[str, object]:
        return {
            "title": title,
            "duration_minutes": 45,
            "tool_time_ceiling_minutes": 8,
            "visual": {
                "label": "Three-state trace",
                "prediction_checkpoint": "What changes next?",
                "kind": "indexed-array-trace",
                "states": [
                    {"step": 1, "array": [1, 2, 3], "i": 0, "message": "Initial state."},
                    {"step": 2, "array": [1, 2, 3], "i": 1, "message": "Second state."},
                    {"step": 3, "array": [1, 2, 3], "i": 2, "message": "Third state."},
                ],
            },
            "questions": [{"kind": "retrieval", "prompt": "What is the invariant?"}],
        }
    return [block("First test block"), block("Second test block")]


def _browser() -> Path:
    configured = os.environ.get("DSA_STUDY_BROWSER")
    if not configured:
        pytest.skip("set DSA_STUDY_BROWSER to a Chromium executable to run browser checks")
    browser = Path(configured)
    if not browser.is_file():
        pytest.skip(f"configured browser does not exist: {browser}")
    return browser


def _probe(*, reduced_motion: bool) -> str:
    """Return browser-mutated DOM after exercising one temporary static page."""
    if reduced_motion:
        checks = """
assert(window.matchMedia('(prefers-reduced-motion: reduce)').matches, 'reduced-motion preference was not applied');
const play = document.querySelector('[data-trace-action="play"]');
assert(play.disabled && play.getAttribute('aria-disabled') === 'true', 'playback remains enabled with reduced motion');
assert(document.querySelector('[data-motion-status]').textContent.includes('Reduced motion is active'), 'reduced-motion status is absent');
const next = document.querySelector('[data-trace-action="step"]');
next.focus(); assert(document.activeElement === next, 'direct Next control cannot receive focus');
next.click();
assert(document.querySelector('[data-current-state]').textContent === '2 of 3', 'direct step control does not work with reduced motion');
report('passed');
"""
    else:
        checks = """
if (location.hash === '#reloaded') {
  assert(document.querySelector('[data-answer-kind]').value === '', 'answer survived a page reload');
  report('passed');
} else {
  const choice = document.querySelector('[data-block="1"]');
  choice.click();
  const selected = document.querySelector('[data-study-block="1"]');
  assert(!selected.hidden, 'block selection did not reveal the selected block');
  assert(document.activeElement === selected.querySelector('h2'), 'focus did not move to the selected block heading');
  const next = selected.querySelector('[data-trace-action="step"]');
  next.focus(); assert(document.activeElement === next, 'Next control cannot receive keyboard focus');
  next.click();
  assert(selected.querySelector('[data-current-state]').textContent === '2 of 3', 'Next did not reveal state two');
  selected.querySelector('[data-trace-action="reset"]').click();
  assert(selected.querySelector('[data-current-state]').textContent === '1 of 3', 'Reset did not restore initial state');
  const answer = selected.querySelector('[data-answer-kind]');
  answer.value = 'private browser-only answer';
  assert(!document.querySelector('form'), 'learner answers unexpectedly have a submission form');
  location.hash = 'reloaded';
  location.reload();
}
"""
    return f"""<script>
(() => {{
  const failures = [];
  const assert = (condition, message) => {{ if (!condition) failures.push(message); }};
  const report = status => {{
    const output = document.createElement('output');
    output.id = 'browser-test-result';
    output.textContent = failures.length ? `failed: ${{failures.join(' | ')}}` : status;
    document.body.append(output);
  }};
  try {{ {checks} }} catch (error) {{ failures.push(error.message); report('failed'); }}
}})();
</script>"""


def _run_probe(tmp_path: Path, *, reduced_motion: bool) -> str:
    browser = _browser()
    site = tmp_path / "site"
    render_site({"topics": [], "problems": []}, site, learning_blocks=_browser_blocks())
    page = site / "index.html"
    page.write_text(page.read_text(encoding="utf-8").replace("</body>", f"{_probe(reduced_motion=reduced_motion)}</body>"), encoding="utf-8")
    profile = tmp_path / ("reduced-profile" if reduced_motion else "default-profile")
    command = [
        str(browser), "--headless", "--disable-gpu", f"--user-data-dir={profile}",
        "--virtual-time-budget=3000", "--dump-dom",
    ]
    if reduced_motion:
        command.append("--force-prefers-reduced-motion")
    command.append(page.as_uri())
    result = subprocess.run(command, capture_output=True, text=True, timeout=20, check=False)
    assert result.returncode == 0, result.stderr
    return result.stdout


def test_browser_trace_focus_and_answer_non_persistence(tmp_path: Path):
    page = _run_probe(tmp_path, reduced_motion=False)
    assert '<output id="browser-test-result">passed</output>' in page


def test_browser_reduced_motion_keeps_direct_trace_controls(tmp_path: Path):
    page = _run_probe(tmp_path, reduced_motion=True)
    assert '<output id="browser-test-result">passed</output>' in page
