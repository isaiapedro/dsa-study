# DSA Study Implementation Plan

This is the canonical grouped plan for work that advances the project’s three
outcomes: DSA foundations, interview-ready problem solving, and professional
transfer. It does not authorize collection, publication, scoring, or profiling
of learner data. Refer to `TASKS.md` for immediate backlog status and
`ROADMAP.md` for milestone status.

## Shared delivery rules

- Keep authored instruction original, local-first, and separate from fetched
  LeetCode material.
- Keep learner answers, confidence, review events, and local solutions in
  ignored Personal local state; never add telemetry or mastery scoring.
- Make motion optional, keyboard operation complete, and every visual meaning
  available in text, table, or semantic HTML/SVG form.
- Treat the local runner as a trusted local check only—not a sandbox or a
  LeetCode-equivalent judge.

## 1. Research

**Purpose:** Establish evidence and a transparent learning sequence without
inferring learner state.

| Priority | Plan | Completion evidence |
| --- | --- | --- |
| High | **Done —** Complete the outstanding DSA-pedagogy, algorithm-visualization, accessibility, and transfer-assessment research queries. See `RESEARCH_SYNTHESIS.md`. | Each source is link-only or held in its governed Knowledge location, with bounded applicability notes. |
| High | **Done —** Define a reviewed curriculum graph: prerequisites, part-of paths, selection dimensions, and close-technique contrasts. See `CURRICULUM_GRAPH.md`. | The map routes each authored block and does not use private progress to infer a next action. |
| High | **Done —** Design an opt-in, private rubric for unseen transfer tasks, invariant explanations, debugging, and trade-off reasoning. See `PRIVATE_TRANSFER_RUBRIC.md`. | Rubric distinguishes attempt, feedback, and outcome; it does not create a mastery score. |
| Medium | **In progress —** Validate the current review-queue heuristic through real local use before changing its intervals or adopting an optimizer. This cannot be substituted by research or synthetic events. | Non-sensitive review record states whether the heuristic is understandable and usable; raw Personal events remain private. |

## 2. Media assets

**Purpose:** Create original, accessible representations that make algorithmic
state and invariants visible.

| Priority | Plan | Completion evidence |
| --- | --- | --- |
| High | Add a reduced-motion path, direct step controls, predictable focus, and browser-level keyboard/accessibility checks. **Done 2026-09-11:** reduced-motion playback suppression, direct controls, focus transfer, and deterministic behavior checks are implemented. | A state-changing visual works without timed playback and its semantic equivalent is tested. |
| High | Add reusable local HTML/SVG/text primitives for binary-search intervals, linked rewiring, stack/queue state, tree returns, graph frontiers, and DP dependencies. **Done 2026-09-11:** semantic text-table primitives now render every authored state type and are covered by deterministic tests. | Each primitive has labelled states, an invariant/prediction checkpoint, reset behavior, and no color-only meaning. |
| Medium | Add constrained, keyboard-equivalent learner input such as choosing a next state or supplying a small trace input. **Done 2026-09-11:** bounded native radio state selection is keyboard-operable, resets with the trace, and remains memory-only. | Input stays in memory, has a non-drag path, and never appears in logs, generated output, or analytics. |
| Deferred | Evaluate external visual sources only for reference. **Done 2026-09-11:** link-only OpenDSA review completed in `MEDIA_ASSET_REVIEW.md`; no asset, embed, or runtime was approved. | Licensing, accessibility, external-runtime, privacy, and retention review is complete before any embed or copied asset is proposed. |

## 3. Code competition

**Purpose:** Turn conceptual blocks into private, interview-relevant problem
solving without copying third-party solutions or overstating local results.

| Priority | Plan | Completion evidence | Status |
| --- | --- | --- | --- |
| High | Build authored blocks for binary search, linked lists, stacks/queues, trees, BFS/DFS, and dynamic programming. | Every block has a model, invariant, visual/trace, prediction, faded scaffold, independent attempt, and exit condition. | **Done — 2026-09-11.** Six original blocks (sequences 4–9) validate with the existing contract. |
| High | Map each block to focused catalog practice using explicit topic/constraint/technique rules. | Selection is explainable and does not depend on an inferred learner profile. | **Done — 2026-09-11.** Fixed project-authored mappings select and rank catalog candidates only by declared tags. |
| Medium | Add interview explanation prompts, edge-case checklists, complexity justifications, and contrast exercises. | A practice attempt includes a stated approach, correctness rationale, time/space claim, and boundary test. | **Done — 2026-09-11.** Local-only prompts cover approach, correctness, complexity, boundary tests, and a close alternative. |
| Medium | Expand local runner fixtures for authored micro-exercises and common node/graph representations. | Fixtures are original and deterministic; runner output remains labelled as local-relative only. | **Done — 2026-09-11.** List, tree, compact adjacency-list, and explicit cyclic graph fixtures are deterministic. |
| Deferred | Add contest-style sets only after the core curriculum and transfer evaluation are working. | Sets preserve source boundaries and do not rely on rankings or public performance claims. | **Deferred — prerequisite not met.** A rubric is documented, but an opted-in private transfer evaluation is not yet working in use; no sets were added. |

## 4. Infrastructure

**Purpose:** Preserve privacy, reproducibility, and reliable local operation.

| Priority | Plan | Completion evidence |
| --- | --- | --- |
| High | **Done — 2026-09-11.** Add browser-level tests for trace interaction, focus, reduced motion, and answer non-persistence. The real-browser suite is opt-in through `DSA_STUDY_BROWSER`; it does not download a browser or add a runtime dependency. | Tests exercise behavior rather than only inspecting generated markup. |
| High | **Done — 2026-09-11.** Reconcile stale status and validation records with the current passing build and block schema. | `STATE.md`, `REVIEW.md`, `RUNNER_VALIDATION.md`, and `AUDIT.md` agree on active blockers and verification results. |
| Medium | **Done — 2026-09-11.** Add a documented manual provider-compatibility check for the unofficial public GraphQL interface. | The check records only response-shape compatibility and aggregate counts. |
| Medium | **Blocked — 2026-09-11.** Re-authenticate the configured private GitHub remote and push the dedicated repository. Existing GitHub tokens are invalid; no interactive authentication, credential change, or push was performed. | Remote access is confirmed without placing credentials in project records. |
| Ongoing | **Done for this change — 2026-09-11.** Run project tests, formatting checks, Registry validation, and a static-site build for relevant changes. | `AUDIT.md` records non-sensitive command outcomes. |

## Delivery order

```text
Infrastructure accessibility baseline
  -> Media primitives
    -> Research-backed curriculum map and private transfer rubric
      -> Code-competition pathways
        -> Review-queue validation and optional advanced features
```

Professional transfer is cross-cutting: each media asset and code-competition
block must include one realistic engineering decision, such as data-model
choice, complexity trade-off, invariant-based debugging, or explanation for a
technical review.
