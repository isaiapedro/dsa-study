# Architectural Decisions

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
