# DSA Study state

## Current status

The academic rewrite now provides 20 written modules, 92 numbered sections,
126 verified catalog-reference links, and a course-first
offline site, with a chapter map covering CLRS 1–35 and A–D plus all numbered
Sedgewick/Wayne sections. Every numbered lesson section includes an original
example, a completion prompt, and LeetCode practice; advanced-topic partial
matches are labeled and supplemented by local exercises. The nine interactive
examples have simpler instructional text and retain their existing controls.
Written coverage is introductory across the books' topics, not a claim to
reproduce every proof or exercise. Drafted questions remain review-required;
automated validation is not a human learning-content review. The course can
build without downloading a catalog. Existing runner and privacy behavior is
unchanged.

Every numbered section now adds one or more direct links to exact printed
textbook pages. The links use lawful Google Books records for the two governed
editions; preview availability remains the rights holder's decision. No
textbook material has been imported or copied into the project.

The project is active, at prototype stage, and implements a local public
catalog synchronizer, topic registry, hardened static site renderer, Python
solution scaffolder, curated CS curriculum, and private progress/review queue.
Its curriculum can now reference the attributed CP-Algorithms source snapshot
held by `knowledge/technology`; the project itself retains no copied source
content. It now includes nine authored interactive foundation blocks rendered
separately from imported catalog material, with controllable accessible traces
and retrieval/transfer prompts. Each block now declares visible curriculum
context and technique-selection dimensions, requires the four-lens pre-code
checkpoint before independent practice, and can carry a bounded advanced bridge
card. Its five release prompts are project-authored and review-required; no
automatic question generation is part of the product. A loopback-only viewer can additionally expose
the local execution harness; it is for trusted local code, not a sandbox or
remote submission path. The review cadence remains intentionally modest and
still requires validation through real local use.

Catalog coverage, example-boundary repair, and the representative local
linear-versus-quadratic runner comparison are documented in
`RUNNER_VALIDATION.md`. Timing is local-relative only, not a LeetCode runtime
proxy. The original three-block schema includes the required
`question_provenance` marker; that historical authoring defect is resolved.
The Code Competition track now supplies fixed, explainable catalog-practice
mappings and local-only interview prompts for all nine blocks. The local runner
also accepts original list, tree, compact adjacency-list graph, and explicit
cyclic-graph fixtures, while remaining a trusted local check rather than a
sandbox or platform-equivalent judge. The current fresh build passes. Provider compatibility
remains an operational check: its reproducible metadata-only procedure is
recorded in `TESTING.md` and `RUNNER_VALIDATION.md`, but a manual public
execution is only needed when a provider change is suspected or before
depending on a new provider response shape.

An interactive-learning assessment reviewed the initial three blocks, their
renderer, local learning evidence, accessibility guidance, and public
comparison assets. The blocks meet the baseline for labelled, non-autoplay
traces and generated prompts. Reduced-motion playback suppression, focus
transfer, and opt-in real-browser behavior tests are now implemented. Those
browser tests run only when an operator supplies an existing Chromium
executable through `DSA_STUDY_BROWSER`; they do not download a browser or
receive learner data. Interactive visual coverage beyond the current blocks
and voluntary private transfer evaluation remain future work. No telemetry,
external embed, or learner data was added. The pre-code answers are ephemeral
browser input and are not written to the project, generated site, catalog,
logs, or Personal progress record.

The resulting implementation work is grouped in `IMPLEMENTATION_PLAN.md` as
Research, Media Assets, Code Competition, and Infrastructure. It is a planning
record only and does not introduce an interface, external provider, retention
period, or learner-data processing.

The completed Research track is recorded in `RESEARCH_SYNTHESIS.md`,
`CURRICULUM_GRAPH.md`, and `PRIVATE_TRANSFER_RUBRIC.md`. The graph is authored
navigation only and the rubric is an unvalidated, opt-in reflective aid. The
review-queue heuristic remains in progress pending voluntary real local use;
no synthetic event or research result has been represented as that validation.

Academic-context assessment now uses two separately governed Technology
textbook records: CLRS for theory/proof/analysis framing and Sedgewick/Wayne
for representation and implementation context. `ACADEMIC_REFERENCE_GUIDELINES.md`
keeps their use link-only and requires original project material.

## Repository and Registry boundary

Implementation, tests, and local configuration belong to the dedicated
`dsa_study` repository. Fetched catalog data, generated site output,
checkpoints, browser state, personal solutions, and progress history are
local-only and excluded from commits and Registry payloads. The Registry owns
only the manifest, repository-boundary declaration, and generated structural
state. The local repository and its `origin` configuration are registered;
remote creation or access still requires renewed GitHub authentication before
the branch can be pushed.

Project-authored learning blocks and their original illustrative examples are
source material and may be versioned with the implementation. They must remain
separate from fetched LeetCode pages and must not persist or render learner
responses, completion, confidence, notes, or review state. The only new
network interface is the documented `127.0.0.1` local endpoint; it introduces
no external provider, account, public exposure, or retention period.
