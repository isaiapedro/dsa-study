# DSA Study testing

## Required verification

For the written course, verify both textbook chapter maps, a practice link
and completion prompt in each numbered section, valid internal module and
section navigation, HTML escaping, and rendering without imported catalog or
learner data. Check LeetCode ID/slug references against local catalog metadata
when available. Partial advanced-topic matches must remain labeled; structural
tests do not establish full mathematical or human pedagogical review.

The course checks live in `tests/test_course.py`. Their fixtures contain only
original text and generated temporary pages; they do not read private progress
or require provider requests. Browser and loopback checks can be skipped by
the environment and must be reported separately from passing static checks.

Run the project test suite after a behavior, storage, or client change:

```bash
cd workspace/side_projects/dsa_study
.venv/bin/python -m pytest
```

Run Registry validation after a manifest, interface, repository, dependency, or
boundary change:

```bash
(cd ../../.. && python3 registry/implementation/cli.py validate)
(cd ../../.. && python3 registry/implementation/cli.py build)
```

Record the date, commands, and outcome in `AUDIT.md`. Mocked GraphQL fixtures
are required for deterministic tests; a manual public sync verifies provider
response compatibility without committing provider content.

## Manual provider-compatibility check

Use this procedure only when the unofficial public GraphQL response shape may
have changed, or before depending on a new provider shape. It is deliberately
manual and must not be added to the normal automated test command.

1. Confirm the run is unauthenticated: no browser cookies, authorization
   headers, account state, or credentials are supplied.
2. Use an ignored local catalog location and run one normal `dsa-study sync`.
   Do not use verbose request/response logging.
3. Run `dsa-study audit` and inspect only aggregate counts and structural
   statuses.
4. Confirm that synchronization completed without a schema/key error, the
   catalog collection is present, and expected catalog identifier, slug, and
   topic metadata fields are available where the provider exposes them.
   Readable, runner-compatible, and unavailable totals must be internally
   consistent; paid-only unavailable details are not a structural failure.
5. Record only date, provider/query class, field-presence pass/fail, aggregate
   counts, and a structural error class if applicable, using the template in
   `RUNNER_VALIDATION.md`. Do not record response bodies, titles, slugs,
   statements, headers, cookies, checkpoints, or terminal output.
6. On failure, stop provider-dependent synchronization and update the client
   plus mocked fixtures under the normal change process before retrying.

This procedure does not verify provider correctness, completeness, access
rights, or stability. It checks only compatibility with the client’s expected
public response shape.

## Learning-block acceptance checks

For each authored block, test that the rendered output includes its invariant
or model, cost/trade-off, original worked trace or visual, prediction,
explanation/contrast, faded scaffold, independent attempt, and exit summary.
Also validate the source contract before rendering: exactly 45 minutes and an
eight-minute tool ceiling; three outcomes; one project-authored,
review-required question for each required kind; visible curriculum path,
prerequisites, and selection dimensions; and the four pre-code lenses
(input/output, constraint, state/invariant, and selection). Test that the
checkpoint renders immediately before independent practice and adds only
ephemeral browser fields.
Each block's fixed catalog-practice mapping must declare a technique, required
topic tags, applicability constraints, and the five local-only interview
prompts (approach, correctness, complexity, boundary test, and contrast).
Test candidate selection with original metadata-only fixtures: required tags
are eligibility rules and preferred tags affect only deterministic ordering.
For every state-changing trace, test semantic keyboard-operable pause,
previous/next, and reset controls plus a textual current-state label and a
non-autoplay initial state. Test that generated output and diagnostics do not
contain submitted responses, completion history, confidence, notes, or other
Personal study state. Use deterministic project-authored fixtures only; never
add fetched LeetCode statements or external course text as test fixtures.

Before adding a new visual kind, extend deterministic tests for its semantic
text/table or SVG equivalent, complete keyboard path, predictable focus after
block selection, and no-motion behavior when a reduced-motion preference is
active. Test the actual browser behavior where feasible, not only generated
markup. Any learner-supplied input must remain in-memory and must not appear in
build output, logs, fixtures, or analytics.

## Loopback execution checks

Test `judge_submission()` for accepted and wrong-answer results, then exercise
`POST /api/run` against a temporary listener bound to `127.0.0.1`. Confirm that
malformed input returns `400`, the command rejects an invalid port, and no test
depends on a public listener, remote judge, or real learner code.
Cover original `ListNode`, `TreeNode`, compact adjacency-list `GraphNode`, and
explicit cyclic-graph fixtures. Assert deterministic canonical graph output;
do not use provider statements, hidden cases, or external solutions.

## Catalog repair and comparison checks

Test that example extraction stops at a subsequent numbered example heading.
When repairing an ignored catalog, record only aggregate repair and residual
contamination counts. Exercise the runner with original implementations and
deterministic, non-provider fixtures; report median aggregate timing only as a
local comparison, never as a LeetCode performance result.
