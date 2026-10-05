# Opt-in private transfer-reflection rubric

Use this only for one unseen, project-authored task in a nearby but non-identical
context. It is a self-review aid, not a score, interview assessment, hiring
signal, ranking, or mastery claim.

## Descriptive dimensions

For each applicable dimension, record one label only: `not attempted`,
`stated`, `evidenced in artifact`, `revised after feedback`, or `not
applicable`. Do not total labels or derive a readiness level.

1. **Problem framing:** input/output, constraints, example behavior, and why a
   naive approach is insufficient.
2. **Representation and selection:** chosen model/technique, closest contrast,
   and required precondition.
3. **Invariant or contract:** pre/postcondition or representation invariant and
   why each operation preserves it.
4. **Trace and prediction:** small unfamiliar trace, decisive next state, and
   relation to the result.
5. **Implementation and boundaries:** original small implementation or
   pseudocode, edge cases, and a boundary test.
6. **Debugging:** failed assumption, guard, or transition; correction; and
   rechecked invariant.
7. **Trade-off explanation:** time, auxiliary space, and the chosen trade-off
   under stated constraints.
8. **Transfer explanation:** why the baseline applies or fails in a realistic
   engineering context, plus one condition required for an advanced extension.

## Required separation

| Record | Purpose | Allowed location |
| --- | --- | --- |
| Attempt | A task/version, optional original trace or solution, and selected feedback dimensions | Browser memory, or ignored `.dsa-study/` only after an explicit save choice |
| Feedback | Descriptive observation, missing condition/boundary, source (`self-check`, authored checklist, or separately opted-in peer/mentor), and optional adjustment | Same private location; never catalog, source, logs, or Registry |
| Outcome | Learner-selected `completed reflection`, `deferred`, `revisit chosen`, or `no outcome recorded` | Same private location; never correctness, score, rank, or confidence adjustment |

No current command writes this rubric. Implementing persistence needs a separate
storage/retention decision, delete/export instructions, tests, and updates to
the contracts named in [IMPLEMENTATION_PATH.md](IMPLEMENTATION_PATH.md). The
review queue must not read rubric records.

## Evidence and limits

This operational design follows the separation of target, attempt, feedback,
and adjustment in [problem-solving practice](../../../knowledge/planning_science/wiki/concepts/problem-solving-practice-and-feedback.md),
[deliberate practice](../../../knowledge/planning_science/wiki/concepts/deliberate-practice.md),
and [retrieval practice](../../../knowledge/planning_science/wiki/concepts/retrieval-practice-and-spaced-review.md).
It is not a validated DSA transfer or interview instrument. The cited evidence
does not justify prediction, profiling, automated next actions, or claims about
an individual's competence.
