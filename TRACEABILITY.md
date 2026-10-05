# DSA Study traceability

## Scope and provenance boundary

The project uses public LeetCode catalog metadata and publicly readable details
through its documented, read-only client. Imported statements are third-party,
reproducible generated material, not project source or Registry content.
Personal solutions and browser/account state are private local material.
The project may reference the separately governed CP-Algorithms source
snapshot at `knowledge/technology/raw/cp-algorithms/`; that corpus remains
objective Technology-domain custody and carries its retained CC BY-SA 4.0
license and attribution requirements.

Learning blocks are project-authored instructional source. Their concepts
trace to `CURRICULUM.md`, the evidence-to-strategy rules in
`LEARNING_EXPERIENCE_DESIGN.md`, and their learning outcomes trace to
`OBJECTIVE.md`. The `curriculum_context` and `pre_code_checkpoint` fields make
the reviewed curriculum relationship and pre-implementation reasoning visible
without collecting learner data.
They may point to a source listed in the curriculum, but they do not inherit
external text, problem statements, examples, or solutions. Learner input,
completion, confidence, and review events are Personal-domain local state;
they have no traceability path into source, generated catalog output, Registry
payloads, or audit records.

## Authoritative records

The 2026-09-11 textbook rewrite is sourced from the governed CLRS and
Sedgewick/Wayne records below and the learning records linked in
`CURRICULUM.md`. `learning_blocks/course.json` is the chapter-to-module map;
the 20 numbered Markdown files are the original academic content;
`course.py` builds their static pages. Hashing, amortized-analysis, and
string-matching wiki records are supporting context within their stated
limits. The official Princeton Context index verified sections 6.1–6.6;
the local textbook contents supplied the remaining chapter metadata.
Practice-link ID/slug pairs were checked against the existing local catalog
without retaining problem statements or solutions. No learner records were
read or used in course selection.

`src/dsa_study/textbook_pages.py` maps every numbered lesson heading to exact
printed page links in the lawful Google Books records for the governed
editions. The map was checked against the local textbook contents; these are
navigation citations, not a public copy, a preview guarantee, or new source
custody.

| Concern | Authority |
| --- | --- |
| Project identity, lifecycle, interfaces | `manifest.yaml` |
| Commit boundary and Git observations | `registry/repositories.yaml` and generated Registry state |
| Work status and planned work | `STATE.md`, `TASKS.md`, `ROADMAP.md` |
| Durable architectural choices | `DECISIONS.md` |
| Governance verification | `AUDIT.md`, `TESTING.md` |
| Operational event policy | `LOGGING.md` |
| Learning-block requirements and concept provenance | `CURRICULUM.md`, `OBJECTIVE.md`, `DECISIONS.md` |
| Textbook-backed academic context and corpus-assessment method | `ACADEMIC_REFERENCE_GUIDELINES.md`, `knowledge/technology/wiki/papers/learning-introduction-to-algorithms-fourth-edition.md`, `knowledge/technology/wiki/papers/learning-algorithms-fourth-edition-sedgewick-wayne.md` |
| Research-query evidence, authored curriculum relationships, and private transfer-reflection design | `RESEARCH_SYNTHESIS.md`, `CURRICULUM_GRAPH.md`, `PRIVATE_TRANSFER_RUBRIC.md` |
| Interactive-learning assessment and source boundary | `LEARNING_EXPERIENCE_DESIGN.md`, `RESEARCH_QUERIES.md`, `AUDIT.md`, `DECISIONS.md` |
| Grouped implementation work and delivery dependencies | `IMPLEMENTATION_PLAN.md`, `TASKS.md`, `ROADMAP.md` |
| Code-competition blocks, fixed practice routing, and interview prompts | `learning_blocks/blocks.json`, `learning_blocks.py`, `render.py`, `tests/test_learning_blocks.py` |
| Local CLI and loopback HTTP interface | `ENDPOINTS.md`, `IMPLEMENTATION_PATH.md`, `server.py`, `runner.py` |
| Runner comparison, local catalog repair, and timing limits | `RUNNER_VALIDATION.md`, `AUDIT.md`, `TESTING.md` |
| External visual-source reference review | `MEDIA_ASSET_REVIEW.md`, `DECISIONS.md`, `AUDIT.md` |
| Public GraphQL shape-only compatibility procedure | `TESTING.md`, `RUNNER_VALIDATION.md`, `LOGGING.md` |

Registry discovery remains structural and path-only; it never indexes imported
or Personal content.

## Interactive-learning assessment sources

The assessment is traceable to `LEARNING_EXPERIENCE_DESIGN.md`,
`RESEARCH_QUERIES.md`, and `AUDIT.md`. Its external references are link-only:
W3C WCAG 2.2 motion guidance, Hundhausen–Douglas–Stasko (2002) on algorithm
visualization, Liu et al. (2024) on algorithm-design pedagogy, and OpenDSA as
a public comparison asset. They inform evaluation and backlog only; no external
source text, image, runtime, account, learner response, score, or analytics
event enters the project.
