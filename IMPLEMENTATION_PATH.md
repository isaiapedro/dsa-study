# Implementation path and data contracts

This is the deterministic handoff document for an LLM agent or maintainer.
Read [AGENTS.md](AGENTS.md), [OBJECTIVE.md](OBJECTIVE.md),
[CURRICULUM.md](CURRICULUM.md), and [TRACEABILITY.md](TRACEABILITY.md) before
changing a path or data contract.

## Three isolated paths

```text
Public catalog: LeetCode client -> catalog normalizer -> data/catalog.json -> renderer -> site/
Authored learning: learning_blocks/blocks.json -> load_learning_blocks() -> renderer -> site/
Private study: CLI progress command -> .dsa-study/progress.json -> review queue only
```

The paths must not merge. `data/` and `site/` are generated/ignored;
`.dsa-study/` and `solutions/` are Personal local state; only authored blocks,
implementation, tests, and contracts are versionable source.

## Add a new authored learning block

1. Choose one curriculum concept and one new interacting element. Do not add
   copied course text, LeetCode statements, complete third-party solutions, or
   learner records.
2. Add one object to `learning_blocks/blocks.json`. Give it a unique `id` and
   the next integer `sequence`.
3. Supply the required fields: `duration_minutes: 45`,
   `tool_time_ceiling_minutes: 8`, three `outcomes` (`foundation`, `interview`,
   `professional_transfer`), `target`, `expected_complexity`, `theory`,
   `curriculum_context`, `visual`, a four-lens `pre_code_checkpoint`, five
   questions, worked example, faded scaffold, independent practice, feedback
   checklist, and exit summary. `curriculum_context` declares the visible
   part-of path, reviewed prerequisites, and selection dimensions. The
   checkpoint asks for input/output, constraints, state/invariant, and technique
   selection before independent coding.
4. The `visual` needs a supported `kind` (`indexed-array-trace`,
   `hash-bucket-trace`, `two-pointer-trace`, `binary-search-interval-trace`,
   `linked-list-rewire-trace`, `stack-queue-trace`, `tree-return-trace`,
   `graph-frontier-trace`, or `dp-dependency-trace`), a label, prediction
   checkpoint, three or more states, and `required_controls` of
   play/pause/step/reset.
   If a new visual kind is necessary, implement a semantic text-equivalent in
   `_render_diagram()` in `src/dsa_study/render.py`; never make color or motion
   the sole carrier of meaning.
5. Keep exactly five project-authored, review-required generative questions
   with kinds `retrieval`, `invariant`, `next-state`, `contrast`, and
   `invalid-use`. Feedback must be concise and must not score mastery. There is
   no automatic question generator in this architecture; any future generator
   must keep proposed content out of published blocks until human review.
6. An optional `bridge_card` may connect the core model to a more advanced
   technique. It must state the extra condition or assumption needed for the
   transfer; it must not turn the 45-minute core block into a survey.
7. Add a fixed mapping in `_PRACTICE_MAPPINGS` in `learning_blocks.py`: a
   technique, required and optional preferred catalog topic slugs, and explicit
   applicability constraints. The loader attaches it and the renderer uses it
   for deterministic candidates and local-only interview prompts; it must not
   use learner state or fetched problem text.
8. Run the verification steps in [OPEN_AND_TEST.md](OPEN_AND_TEST.md). Extend
   deterministic tests whenever a new renderer behavior or schema rule is
   introduced.

## Use the local runner with structured fixtures

`runner.py` accepts JSON arrays for `ListNode` and level-order `TreeNode`
fixtures. `GraphNode` accepts either a compact one-based adjacency list or an
explicit `{root, nodes}` object; cyclic graph output is converted to a stable
breadth-first JSON form. These are original local fixtures for micro-exercises,
not imported provider cases or a secure judge.

## Add or change imported catalog data

Only `src/dsa_study/client.py` may select public provider query shapes. The
flow is `client.py` -> `catalog.py` normalization -> ignored `data/catalog.json`
-> `render.py`. Preserve the paid-only and public-readability checks, sanitize
statement markup with `html_tools.py`, and never put fetched content in source,
fixtures, learning blocks, audit logs, or Registry records.

## Add private learning data

Use `progress.py` and `storage.progress_path()` only. It writes ignored
`.dsa-study/progress.json`; `review` derives its queue in memory. Do not add
private input to `blocks.json`, catalog records, static HTML, telemetry, or
logs. A new Personal field requires an explicit storage/retention decision in
`DECISIONS.md` and matching updates to traceability, logging, and tests.

## Add a local interface

Prefer a CLI command for local tasks. A network endpoint must bind only to
`127.0.0.1`, document request/response behavior in [ENDPOINTS.md](ENDPOINTS.md),
have deterministic endpoint tests, avoid logging bodies, and be described as
local execution rather than a security sandbox. Provider, account, public
network, or retention changes require a decision record and Registry review.

## Implementation acceptance gate

Before handoff: run the full test suite, build the site, run `git diff --check`,
and run Registry validation/build when boundaries, manifest interfaces, or
dependencies change. Record non-sensitive results in `AUDIT.md`.
