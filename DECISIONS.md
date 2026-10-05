# Architectural Decisions

## 2026-09-11 — Textbook topics become a written course

The user requested a plain-language rewrite covering both reference books.
Twenty original Markdown modules now form the main course. A chapter map in
`learning_blocks/course.json` connects all CLRS chapters and appendices and
all Sedgewick/Wayne numbered sections. Nine existing interactive examples
remain supplementary and retain stable internal identifiers and controls.
The short learning-session sequence applies to individual sections; advanced
chapters receive their own lessons, superseding the earlier bridge-only
presentation restriction for this scope.

The renderer builds escaped, static course pages without new dependencies,
external assets, data collection, or Knowledge ingestion. Builds can use an
empty catalog. The source records guide scope and qualified claims; authored
course text does not reproduce textbook passages or exercises. LeetCode
references are verified metadata links, with direct and partial-topic practice
distinguished in the lessons. Full topical breadth is not a claim to reproduce
every book proof, implementation, or exercise, and automated checks do not
replace human review of drafted questions.

## 2026-09-11 — Registry updates are complete governance updates

An instruction to update this folder's Registry means updating all applicable
project, boundary, status, roadmap, task, decision, audit, provenance, logging,
and testing records—not just `manifest.yaml`. The completion gate is defined in
`REGISTRY_UPDATE.md`. This standard preserves local-only generated and Personal
material while making the project’s durable controls auditable.

## 2026-09-11 — DSA Study owns an independent repository boundary

The project now has a dedicated local Git repository registered as
`dsa_study`. Its source, tests, contracts, and local configuration belong to
that repository; the root PIOS repository excludes it. Fetched catalog data,
generated site output, checkpoints, browser state, and personal solutions stay
local and excluded. The configured remote name and URL are declarative routing
metadata only; no remote mutation is performed by Registry adoption.

## 2026-09-01 — Own a small public GraphQL synchronizer

**Decision:** Use an isolated, read-only LeetCode GraphQL client instead of a
third-party CLI as the project data interface.

**Reason:** Interactive CLIs are useful for solving one problem but do not
provide a stable bulk-export contract and still depend on LeetCode's web
queries. Keeping the two query shapes in this project makes the catalog
reproducible, testable, and replaceable.

**Consequences:** The client pages catalog metadata, then fetches readable
details per slug with checkpoints, rate limiting, and response validation.

## 2026-09-01 — Keep external content generated and local

**Decision:** Ignore fetched statements, generated pages, checkpoints, and
personal solutions.

**Reason:** Avoid committing third-party problem content, personal work, or
account-related state.

**Repository contract:** The root default-deny Git policy explicitly permits
this project's source, tests, and contracts while continuing to exclude its
generated catalog, site, checkpoints, and solutions.

## 2026-09-01 — Derive the topic registry from the complete catalog

**Decision:** Build the rendered topic registry from the union of official
`topicTags`, keyed by stable slug rather than a hand-maintained partial list.

## 2026-09-11 — Keep curated CS guidance authored and link-only

**Decision:** Store project-authored concept notes and curated external reading
links in `CURRICULUM.md`, outside the generated LeetCode catalog and static
site paths. Do not mirror or ingest external reading material by default.

**Reason:** A small, reviewable curriculum gives the study workspace durable
conceptual guidance without mixing third-party LeetCode material, external
copyrighted text, personal progress, or solution history into its source.

**Consequences:** Curated sources are represented by a title, purpose, and URL.
They can be reviewed or replaced independently of catalog synchronization;
future imported material requires an explicit licensing and storage decision.

## 2026-09-11 — Reference the CP-Algorithms corpus from Technology Knowledge

**Decision:** Keep the DSA Study repository link-only, while referencing the
attributed CP-Algorithms source snapshot held in
`knowledge/technology/raw/cp-algorithms/`.

**Reason:** The source is relevant to the curriculum, but a shared objective
Knowledge corpus prevents third-party material from being copied into the
project repository or mixed with local solutions and generated catalog data.

**Consequences:** The Technology source record preserves the source commit,
attribution, and CC BY-SA 4.0 license. Project-authored notes may cite it;
they must not reproduce or adapt its text without preserving applicable
attribution and share-alike obligations.

## 2026-09-11 — Keep progress and review scheduling in private local state

**Decision:** Store append-only study events, optional notes, and derived
review queues under `.dsa-study/progress.json`; do not merge them into the
catalog or static site.

**Reason:** Progress, confidence, and notes are Personal-domain observations.
They must not be published with imported LeetCode material or cross the
unmanaged repository boundary.

**Consequences:** `dsa-study progress` records local events and
`dsa-study review` derives a transparent confidence-based queue at runtime.
The heuristic is intentionally modest and can evolve without migrating
published data.

## 2026-09-11 — Render authored learning blocks as a local, separate layer

**Decision:** Add project-authored interactive learning blocks alongside, but
structurally separate from, the generated LeetCode catalog. Blocks teach a
single curriculum concept through an original visual or worked trace,
prediction and explanation prompts, scaffolded practice, an independent
attempt, and an exit summary.

**Reason:** The catalog supports discovery, while the study objective requires
observable reasoning about invariants, state, complexity, correctness, and
transfer. Keeping the layer authored and separate preserves copyright and
privacy boundaries.

**Consequences:** State-changing visuals require pause/step/reset controls and
text equivalents; controls must work by keyboard. Block content may use only
original minimal examples or links to approved sources, not imported problem
text or solutions. Any learner-entered response or completion signal remains
ephemeral or in ignored local state, is excluded from generated catalog pages,
and is never interpreted as public mastery evidence.

## 2026-09-11 — Keep the execution harness loopback-only and explicitly non-sandboxed

**Decision:** Serve the generated site and `POST /api/run` only on
`127.0.0.1`, with no authentication, persistence, remote submission, or
request-body logging.

**Reason:** Local code execution can support small, reproducible study checks,
but submitted code and test cases may be private and arbitrary. Loopback scope
and an explicit trusted-code warning avoid representing this feature as a
secure judge or an external service.

**Consequences:** The server is documented in `ENDPOINTS.md`, tested through a
temporary loopback listener, and started only by `dsa-study serve`. It must not
be rebound to a public interface without a separate product, security,
retention, and Registry decision.

## 2026-09-11 — Make learning-strategy safeguards structural block fields

**Decision:** Require each authored learning block to declare visible
curriculum context and a four-lens pre-code checkpoint, retain exactly five
project-authored review-required prompts, and allow an optional, bounded
advanced bridge card.

**Reason:** The local learning corpus supports making problem interpretation,
invariants, selection rationale, close-method contrasts, and progressive
extensions explicit. Representing these as validated source fields is more
reliable than relying on a prose template alone.

**Consequences:** `learning_blocks.py` rejects incomplete authored blocks
before rendering. The static page renders the checkpoint immediately before
independent practice. No question generator, learner profiling, completion
scoring, storage, telemetry, or external source content is introduced.

## 2026-09-11 — Keep research artifacts declarative and non-assessive

**Decision:** Record the query synthesis and reviewed curriculum graph as
project-authored, link-only guidance. Provide a private transfer-reflection
rubric as an unvalidated specification only; do not implement persistence,
scoring, learner modeling, or automated sequencing.

**Reason:** The local and link-only evidence supports explicit instructional
relationships and low-stakes reflection, but does not validate an individual
transfer, interview, or mastery assessment. Review-queue usability also
requires voluntary real use rather than synthetic records.

**Consequences:** `RESEARCH_SYNTHESIS.md`, `CURRICULUM_GRAPH.md`, and
`PRIVATE_TRANSFER_RUBRIC.md` remain authored documentation. Any feature that
writes rubric data requires a separate Personal-storage decision and matching
traceability, logging, retention, and test changes. The review queue stays
independent of the rubric.

## 2026-09-11 — Use governed textbooks as link-only academic references

**Decision:** Use the separately governed CLRS and Sedgewick/Wayne textbook
records to assess academic coverage and structure project-authored instruction.
Keep their raw files in Technology Knowledge; the DSA project retains only
original guidelines and links.

**Reason:** The two texts complement one another: CLRS provides theoretical
models, correctness, and analysis framing, while Sedgewick/Wayne offers
implementation-oriented representations and trace context. Their copyrighted
content must not enter authored blocks or catalog paths.

**Consequences:** `ACADEMIC_REFERENCE_GUIDELINES.md` defines the required
source matrix and focus order. Textbook prose, figures, exercises, code,
pseudocode, answers, and book-site resources are excluded unless a later
copyright decision specifically authorizes reuse. They do not license learner
profiling, scoring, or a new external runtime.

## 2026-09-11 — Expand interaction through original local-first primitives

**Decision:** Treat current HTML state traces as the baseline and extend them
with original, semantic local primitives—not copied images, autoplay media, or
remote visualization embeds. Motion is an optional representation of a state
transition, never the only carrier of a concept.

**Reason:** The assessment found that the project already has appropriate
prediction, feedback, and controlled stepping for three foundations, while its
main gaps are topic coverage, reduced-motion handling, and behavior-level
accessibility verification. External projects such as OpenDSA are useful
link-only design references, but an embed would introduce an external runtime
and potentially different storage, availability, and accessibility behavior.

**Consequences:** New visuals must provide an original labelled HTML/SVG or
text/table representation, native keyboard operation, direct stepping, reset,
and an input alternative to drag-only manipulation. They must respect a user
motion preference or provide a no-motion route. No third-party visual asset,
iframe, analytics SDK, score reporting, or learner record may be added without
a separate licensing, privacy, retention, and external-service decision.

## 2026-09-11 — Keep runner comparisons local, original, and non-equivalent to LeetCode

**Decision:** Validate the local runner with original implementations and
synthetic inputs, record only aggregate local results, and retain public forum
research as URLs without copied code or prose.

**Reason:** The local harness can check supplied outputs and reveal practical
growth-rate differences, but it has neither LeetCode's hidden suite nor its
execution environment. Treating local milliseconds as a platform result would
misrepresent the evidence and retaining third-party solutions would violate the
project's source boundary.

**Consequences:** `RUNNER_VALIDATION.md` records method, aggregate results,
source URLs, and limitations. The runner must label timing as local-relative;
it must not show a LeetCode percentile, time-limit prediction, or claim of
submission equivalence. Public examples may be repaired only from ignored local
statement markup, never from copied external solution material.

## 2026-09-11 — Use fixed code-competition routing and original structured fixtures

**Decision:** Connect each authored learning block to catalog practice through
project-authored topic, constraint, and technique rules; render local-only
interview prompts; and support original list, tree, and graph runner fixtures.

**Reason:** Interview practice needs a reviewable route from a concept to a
problem type, and common structures need small deterministic local exercises.
Fixed rules are auditable and avoid learner profiling; structured fixtures make
the runner useful without importing provider cases or claiming platform parity.

**Consequences:** Preferred topic tags only rank already eligible catalog
candidates. Prompt text remains browser-memory-only. Graph results use a stable
explicit JSON form, including cycles. Contest-style sets remain deferred until
an opted-in private transfer evaluation is working in use; no ranking, telemetry,
third-party solution, or public performance claim is introduced.
