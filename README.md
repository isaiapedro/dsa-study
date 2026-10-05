# DSA Study

An offline, Python-first workspace for studying data structures, algorithms,
and LeetCode problems. It keeps the implementation and personal solutions
local; no credentials or fetched problem statements are committed.

## Study objective

See [OBJECTIVE.md](OBJECTIVE.md) for the learning direction: DSA fundamentals,
interview-ready problem solving, and professional application. The detailed
comparison with Personal long-term goals remains in the Personal domain.

## Setup

```bash
cd workspace/side_projects/dsa_study
python3 -m venv .venv
.venv/bin/python -m pip install -e . pytest
```

## Workflow

```bash
# Fetch the public catalog and publicly readable details. Safe to re-run.
dsa-study sync

# Continue a stopped detail pass.
dsa-study sync --resume

# Generate site/index.html for offline browsing.
dsa-study build

# Report coverage and repair local extracted examples without provider access.
dsa-study audit
dsa-study repair-examples

# Serve the generated site and the loopback-only local runner.
dsa-study serve

# Create local Python solution and test skeletons for a fetched problem.
dsa-study new-solution 1

# Record a local-only attempt, solution, or review. Notes stay private.
dsa-study progress 1 --status solved --confidence 3 --note "Revisit complement lookup"

# Show due reviews; --all includes future scheduled reviews.
dsa-study review --all
```

The public catalog lists paid-only problems but does not attempt to bypass
access controls. Their metadata remains visible and their statement state is
shown as unavailable.

Progress events and review queues live only in `.dsa-study/progress.json`.
They are deliberately neither rendered into `site/` nor added to the imported
catalog, and are ignored by Git.

## Curated study material

Project-authored concept notes and external reading links live in
[CURRICULUM.md](CURRICULUM.md). They are tracked separately from the ignored,
fetched LeetCode catalog and generated site output.

Start with [the course contents](CURRICULUM.md): 20 textbook-style modules
cover the chapter topics of CLRS and Sedgewick/Wayne, including the advanced
chapters and mathematical background. Each numbered section explains an idea,
walks through a small example, asks you to complete a step, and links to exact
textbook pages plus LeetCode practice. Related exercises are labeled when they cover only part of
an advanced topic.

The site opens with the course and provides a separate page for every module.
Nine interactive examples below the contents let you predict and step through
arrays, hashing, pointers, searching, lists, trees, graphs, and dynamic
programming. Use one section for a focused session and return later to recall
the idea. The drafted prompts retain their review-required status.

## Reproducible handoff

- [Open and test](OPEN_AND_TEST.md) provides the complete local verification
  sequence.
- [Implementation path](IMPLEMENTATION_PATH.md) defines how authored,
  imported, and private data connect without crossing their boundaries.
- [Local interfaces](ENDPOINTS.md) documents every CLI and HTTP interface,
  including the loopback-only execution API.
- [Runner validation](RUNNER_VALIDATION.md) records catalog integrity,
  comparison methodology, results, and timing limitations.
