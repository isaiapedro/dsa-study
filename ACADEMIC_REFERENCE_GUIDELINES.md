# Academic reference guidelines

## Purpose and boundary

Use the two governed textbooks as complementary reference anchors when
assessing the Knowledge corpus and authoring the DSA Study application:

- [CLRS fourth-edition record](../../../knowledge/technology/wiki/papers/learning-introduction-to-algorithms-fourth-edition.md)
  anchors theory: models, proofs, invariants, asymptotic analysis, and broad
  algorithm families.
- [Sedgewick and Wayne fourth-edition record](../../../knowledge/technology/wiki/papers/learning-algorithms-fourth-edition-sedgewick-wayne.md)
  anchors practical representations: operations, traces, APIs, test cases, and
  implementation trade-offs.

The raw textbook files remain Technology Knowledge custody. This project uses
only original, concise explanations and links to the records. It must not copy
or adapt textbook prose, pseudocode, code, exercises, figures, answer keys, or
book-site resources without a separate copyright review.

## How to assess a knowledge topic

For each proposed block or application feature, create a short source matrix:

| Question | Academic focus | Required outcome |
| --- | --- | --- |
| What is the formal problem and model? | CLRS | Input/output, preconditions, and cost model stated. |
| What representation and operation make it concrete? | Sedgewick/Wayne | Small original state trace and operation contract. |
| Why is the approach correct? | CLRS | Invariant, termination/correctness argument, or proof condition. |
| How is it used and tested locally? | Sedgewick/Wayne | Original boundary cases, complexity explanation, and local-only exercise. |
| What complements or limits it? | Both plus governed papers/CP-Algorithms | Close-technique contrast and one named assumption. |

Mark a topic **ready for authored instruction** only when all five outcomes are
present in project-authored language. A source existing in the database is not
enough by itself; the record must identify its scope and limit.

## Application focus order

The 2026-09-11 rewrite implements the user's full-textbook-topic request as
20 written modules, with the chapter map in `CURRICULUM.md` and
`learning_blocks/course.json`. The nine interactive blocks are supplementary
examples, not the whole course. Advanced chapters now receive their own
lessons rather than being confined to bridge cards. A 45-minute session
applies to one section or exercise, not an entire module. All explanations,
examples, and exercises remain original; topical coverage does not claim to
reproduce every textbook proof, listing, or exercise.

Student-facing text uses a definition, a worked example, a completion prompt,
practice, and later recall. Keep source-assessment matrices and operational
contracts in authoring records. Retain essential terms such as invariant,
amortized, and residual edge only with a plain explanation. Do not describe
all wiki records as scientifically proved: textbook theorems, instructional
notes, surveys, and learning studies have different scopes and limits.

Every numbered course section has direct page links for the relevant textbook
edition. They use the official-edition Google Books records and exact printed
page numbers as lawful navigation links. A rights-holder may limit preview;
the links are not a source of copied material and do not alter raw-source
custody or the project's link-only policy.

1. **Foundations:** representation, contracts, loop invariants, asymptotic
   analysis, recursion, and testing of boundary cases.
2. **Core structures:** arrays, linked structures, stacks/queues, hashing,
   trees/heaps, and disjoint sets; emphasize operation invariants and trade-offs.
3. **Algorithmic techniques:** sorting/searching, divide and conquer, greedy
   proofs, dynamic-programming state/transition design, and randomized
   assumptions.
4. **Graphs and strings:** representation choice, traversal frontier/finish
   state, shortest-path preconditions, and preprocessing/query trade-offs.
5. **Advanced extensions:** only after the sequential baseline is explicit;
   name changes in update model, memory, passes, probability, or approximation.

Each 45-minute block stays narrow: one model, one maintained state or
invariant, one labelled visual trace, one close contrast, and one original
transfer attempt. Textbooks inform scope; the project’s learning evidence
continues to govern retrieval, feedback, fading, and privacy boundaries.

## Database-review checklist

- Prefer the textbook record for breadth/canonical framing, the CP-Algorithms
  record for an attributed implementation reference, and bounded research
  records for specialized or pedagogical claims.
- Separate a theoretical statement, an implementation observation, and a
  learning-design claim; they require different evidence.
- Record page/chapter/topic metadata only when useful. Never retain copied
  passages or use copyright status as evidence of correctness.
- Do not use source coverage, time on task, quiz answers, confidence, or review
  events to infer readiness, select a next topic, or claim mastery.
- Keep generated catalog content and Personal learner state outside this
  reference path.
