# Research synthesis and query disposition

This is a project-authored, link-only synthesis. It neither copies external
instructional content nor records learner data. It supports design constraints,
not claims of individual learning gain, interview readiness, or an optimal
study schedule.

## Completed query groups

| Query group | Evidence location or link-only source | Design disposition and limit |
| --- | --- | --- |
| Correctness, invariants, and proof | [Learning Loop Invariants](https://par.nsf.gov/biblio/10195158-learning-loop-invariants); [verified-programs record](../../../knowledge/technology/wiki/papers/learning-a-textbook-of-verified-ocaml-programs-a-deductive-study-on-algorithms-and-data-structure.md) | Use explicit pre/postconditions and invariants before code. The cited SIGCSE item identifies difficulties; it does not validate this product's checkpoint. |
| Amortized analysis, hashing, and union-find | [amortized-analysis record](../../../knowledge/technology/wiki/papers/learning-two-decades-of-automatic-amortized-resource-analysis.md), [universal-hashing record](../../../knowledge/technology/wiki/papers/learning-uniform-and-universal-hashing.md), and [CP-Algorithms corpus](../../../knowledge/technology/wiki/papers/cp-algorithms-corpus.md) | Support content boundaries and qualified cost claims only; they are not learning-effect evidence. |
| Dynamic programming and greedy proof | [worked-example DP study](https://doi.org/10.1145/3545947.3576232), [DP-misconception replication](https://doi.org/10.1080/08993408.2022.2079865), and [greedy-misconception study](https://www.researchgate.net/publication/261490606_Identification_and_removal_of_misconceptions_about_greedy_algorithms_assisted_by_an_interactive_system) | Use recurrence/base-case and proof-condition prompts. Small or context-specific studies do not establish an optimal block design. |
| Graphs, matching, ranges, strings, and dynamic graphs | [learning corpus index](../../../knowledge/technology/wiki/learning-corpus-ingestion-index.md), [dynamic-graph record](../../../knowledge/technology/wiki/papers/learning-dynamic-graph-algorithms-for-connectivity-problems.md), [dynamic-shortest-path record](../../../knowledge/technology/wiki/papers/learning-dynamic-shortest-path-and-transitive-closure-algorithms-a-survey.md), and [string-matching survey](../../../knowledge/technology/wiki/papers/learning-a-survey-of-string-matching-algorithms.md) | Define baseline topics and advanced bridge assumptions; do not turn survey coverage into a learner sequence claim. |
| Worked examples, retrieval, and close contrasts | [worked-example design record](../../../knowledge/planning_science/wiki/papers/learning-exploring-design-characteristics-of-worked-examples-to.md), [retrieval record](../../../knowledge/planning_science/wiki/papers/learning-retrieval-practices-enhance-computational-and-scientific-thinking-skills.md), and [interleaving review](../../../knowledge/planning_science/wiki/papers/learning-a-systematic-review-of-interleaving-as-a-concept-learning-strategy.md) | Retain model → faded scaffold → independent attempt; retrieve → feedback; and contrasts between close techniques only. Do not infer a learner-specific schedule. |
| Algorithm visualization | [Hundhausen, Douglas, and Stasko meta-study](https://users.cs.duke.edu/~rodger/jflappapers/Hundhausen2002.pdf) and [scientific-visualization record](../../../knowledge/technology/wiki/papers/learning-scientific-visualization.md) | Require prediction, state labels, and feedback; animation alone is not treated as sufficient or as a demonstrated learning effect. |
| Accessibility and external assets | [W3C WCAG 2.3.3](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html), [W3C WCAG 2.2.2](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html), and [OpenDSA about](https://opendsa.org/home/about) | Respect reduced-motion preferences; provide pause/step/reset and semantic non-motion state equivalents. W3C guidance is an accessibility constraint, not pedagogy evidence; OpenDSA is comparison-only. |
| Transfer assessment | [problem-solving practice](../../../knowledge/planning_science/wiki/concepts/problem-solving-practice-and-feedback.md), [programming-difficulty review](../../../knowledge/planning_science/wiki/papers/learning-factors-contributing-to-the-difficulties-in-teaching-and-learning-of-computer-programming-a-literature-review.md), and [computational-thinking transfer study](https://www.mdpi.com/2227-7102/14/9/980) | Use a private, descriptive reflection rubric. No located source validates a DSA rubric as an interview, hiring, or mastery instrument; the rubric remains deliberately non-scoring. |

## Disposition of the query register

The twenty queries in [RESEARCH_QUERIES.md](RESEARCH_QUERIES.md) have been
reviewed through the sources above and the governed learning-corpus index.
Query completion means a source or a documented evidence gap is available; it
does **not** mean that every topic has a product-ready block or that the source
validates an outcome claim. The remaining implementation work belongs to the
Media Assets and Code Competition sections of
[IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md).

## Evidence limits retained by the project

- Topic-specific DSA pedagogy evidence is uneven. The project therefore uses
  explicit instructional safeguards rather than claiming a proven universal
  sequence.
- Transfer research located here is adjacent computational-thinking evidence,
  not validation of a DSA interview assessment.
- Accessibility requirements constrain the interface independently of whether
  a visualization is educationally effective.
- No source authorizes learner profiling, automated sequencing, telemetry,
  mastery scoring, or external content ingestion.
