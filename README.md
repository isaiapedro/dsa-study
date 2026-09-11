# DSA Study

An offline, Python-first workspace for studying data structures, algorithms,
and LeetCode problems. It keeps the implementation and personal solutions
local; no credentials or fetched problem statements are committed.

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

# Create local Python solution and test skeletons for a fetched problem.
dsa-study new-solution 1
```

The public catalog lists paid-only problems but does not attempt to bypass
access controls. Their metadata remains visible and their statement state is
shown as unavailable.

## Curated study material

Project-authored concept notes and external reading links live in
[CURRICULUM.md](CURRICULUM.md). They are tracked separately from the ignored,
fetched LeetCode catalog and generated site output.
