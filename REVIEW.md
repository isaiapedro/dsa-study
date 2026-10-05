# Project Review

## Scope reviewed

The active prototype provides a local public-catalog synchronizer, canonical
topic registry, static study site, Python solution scaffolding, private local
progress/review queue, three project-authored learning blocks, and a
loopback-only trusted-code runner. The rendered blocks are arrays/indexing,
hash-table collision reasoning, and two pointers. They load from the
versioned `learning_blocks/blocks.json` schema and remain separate from
ignored imported catalog material and Personal study state.

## Current validation position

Deterministic fixtures are the authority for normal tests. The learning-block
contract validates project-authored provenance, 45-minute structure,
curriculum context, five review-required prompts, pre-code reasoning lenses,
and controlled trace state. The local runner is verified as a loopback-only
trusted local check; it is not a security sandbox, remote judge, or a source
of LeetCode-equivalent performance claims.

The prior record that the original three blocks lacked `question_provenance`
is stale: that schema supplies it for all three blocks. The binary-search and
subsequent block mappings now supply their required technique, topic-tag, and
constraint fields, so the current deterministic suite and fresh site build
pass. Browser-level reduced-motion, focus, keyboard-trace, reset, and answer
non-persistence checks are implemented as an opt-in Chromium suite; an
operator supplies `DSA_STUDY_BROWSER` rather than the project downloading a
browser. Markup-only checks remain supplemental rather than a substitute for
that behavior suite.

## Review-queue usability validation

**In progress; no conclusion recorded.** The heuristic is deterministic and
unit-tested, but interval changes require voluntary real local study use. This
record must contain only a non-sensitive conclusion about whether the queue was
understandable and usable; it must not contain event history, notes, confidence,
problem identifiers, or learner outcomes. Synthetic events and research sources
are not substitutes for this validation.

## Provider compatibility routine

Do not make routine tests depend on the unofficial public GraphQL provider.
When a provider change is suspected, or before relying on a new provider
shape, follow the metadata-only procedure in `TESTING.md` and record its
outcome in `RUNNER_VALIDATION.md`. The check may retain only endpoint/query
class, pass/fail, response-shape field presence, and aggregate record counts.
It must never retain response bodies, titles, slugs, statements, cookies,
headers, account state, or other request payloads.
