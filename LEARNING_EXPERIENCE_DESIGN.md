# DSA Learning Experience Design

## Purpose and boundary

Current application (2026-09-11): the user's textbook rewrite uses 20 written
modules as the main course and nine interactive examples as supplements.
Apply the short-session sequence below to one numbered section at a time.
Advanced material has dedicated sections; the earlier bridge-only restriction
does not limit this requested textbook coverage. Preserve the teaching steps
while keeping authoring terminology and governance notes out of lesson prose.

This specification defines a concise, repeatable learning block for the DSA
Study experiment. It connects conceptual understanding, implementation
practice, and LeetCode work without treating a completed exercise, elapsed
time, or tool activity as evidence of mastery.

Each block addresses one subtopic—such as a binary-search invariant, BFS
frontier, hash-table collision, or dynamic-programming transition—and must be
small enough for one focused session.

## Evidence basis and limits

The normative rules below are grounded in local, bounded concept records:

- [`retrieval-practice-and-spaced-review`](../../../knowledge/planning_science/wiki/concepts/retrieval-practice-and-spaced-review.md): separate exposure, retrieval attempt, feedback, and later review.
- [`problem-solving-practice-and-feedback`](../../../knowledge/planning_science/wiki/concepts/problem-solving-practice-and-feedback.md): use modelling, scaffolding, feedback, and fading to make strategy visible.
- [`deliberate-practice`](../../../knowledge/planning_science/wiki/concepts/deliberate-practice.md): name the target, feedback source, and next adjustment.
- [`cognitive-load-sweller-1988`](../../../knowledge/health/wiki/papers/cognitive-load-sweller-1988.md): introduce interacting elements progressively and couple text to the relevant diagram or code.
- [`interleaving-kornell-bjork-2008`](../../../knowledge/health/wiki/papers/interleaving-kornell-bjork-2008.md): briefly contrast easily confused techniques.

The following newly curated records refine implementation choices while keeping
their stated limits:

- The [interleaving review](../../../knowledge/planning_science/wiki/papers/learning-a-systematic-review-of-interleaving-as-a-concept-learning-strategy.md)
  supports contrasts among related techniques, not arbitrary topic switching.
- The [worked-examples study](../../../knowledge/planning_science/wiki/papers/learning-exploring-design-characteristics-of-worked-examples-to.md)
  supports a novice-oriented model → completion → independent sequence, with
  self-explanation prompts as a design hypothesis rather than a universal rule.
- The [computational-thinking retrieval study](../../../knowledge/planning_science/wiki/papers/learning-retrieval-practices-enhance-computational-and-scientific-thinking-skills.md)
  supports retrieval prompts and distributed revisit opportunities; it does not
  establish an individual learning gain.
- The [programming-difficulty review](../../../knowledge/planning_science/wiki/papers/learning-factors-contributing-to-the-difficulties-in-teaching-and-learning-of-computer-programming-a-literature-review.md)
  supports explicit treatment of abstraction, problem interpretation, and
  algorithm construction.
- The [LLM-question study](../../../knowledge/planning_science/wiki/papers/learning-enhancing-student-learning-with-llm-generated-retrieval-practice-questions-an-empirical-study-in-data-science-courses.md)
  permits assisted question drafting only with human review; generated questions
  must not be treated as automatically reliable.

The block design must not use learning-style labels, learner personas, or an
automated recommendation system to profile a learner or infer readiness.

## Evidence-to-strategy map

The new corpus strengthens the strategy in two different ways: learning studies
inform the *instructional sequence*; algorithm sources inform the *content
scope, visual model, and exercise boundary*. They do not turn a study block
into a personalized scoring system.

| Evidence relationship | Strategy update | Implementation rule |
| --- | --- | --- |
| Related-category interleaving | Contrast only methods that solve nearby structures, such as BFS/DFS, prefix sum/sliding window, or Dijkstra/Bellman–Ford. | The contrast prompt names the distinguishing precondition; do not mix unrelated topics merely for variety. |
| Generation and retrieval | Ask for a prediction before revealing a trace transition, then give feedback. | Each visual has one answerable next-state question, not a passive autoplay sequence. |
| Faded worked examples | Make the first trace explicit, remove one meaningful step in the next trace, then give an independent transfer task. | The missing step must be an invariant, guard, boundary case, or transition—not cosmetic syntax. |
| Programming-learning difficulties | Add an interpretation gate before coding. | Learner states input, output, constraints, example behavior, and the candidate state/invariant before opening an editor. |
| Code + conceptual context | Pair the code trace with the problem condition and complexity argument. | A block cannot show code alone; it must show the state representation and why the operation preserves it. |
| Drafted retrieval questions | Generation may accelerate authoring, but not validation. | Every generated question needs a human-verified answer, target concept, difficulty label, and source/solution check before release. |
| Prerequisite graphs | Represent curriculum relations transparently rather than inferring them from learner data. | Declare reviewed `requires` and `part_of` edges in the curriculum; never auto-promote or label a learner. |
| Invariants/specifications | Treat a precondition, postcondition, and representation invariant as first-class learning artifacts. | Add one short “contract before code” insertion to structure-heavy blocks such as hash tables, DSU, trees, and range structures. |
| Algorithm-selection taxonomies | Select exercises through explicit problem dimensions. | For graphs, label query type, graph constraints, and candidate technique before the exercise; for hashing, label collision/load/randomness assumptions. |
| Advanced research boundaries | Keep concurrent, dynamic, streaming, probabilistic, and geometry results as optional extensions. | Core blocks use sequential, explicit-input baselines first; extensions compare assumptions, preprocessing, memory, passes, approximation, or update model. |

### Required pre-code insertion

Before every LeetCode or authored implementation exercise, insert this
four-line checkpoint:

```text
Input / output: What is given and what must be returned?
Constraint: Which bound or property rules out the naïve approach?
State: What information must remain true while the algorithm runs?
Selection: Why does this technique fit better than its closest alternative?
```

The feedback step checks this checkpoint before checking code. This makes
problem interpretation and algorithm selection visible, while retaining the
existing stop rule: a block records an attempt and correction, not a mastery
judgement.

### Advanced-topic treatment

Use the algorithm corpus to create short *bridge cards*, not oversized core
blocks. Examples include: why deletion breaks ordinary union-find; why dynamic
shortest paths differ from rerunning Dijkstra; why a streaming matching method
trades exactness for passes and memory; why universal-hashing guarantees depend
on assumptions; and why amortized analysis describes a sequence rather than a
single operation. Each bridge card links back to a simple baseline and ends in
one comparison question.

Historical visualization material can justify the role of an interactive state
representation, but not a learning-effect claim. Therefore animations remain
subject to the existing prediction, pause/step/reset, and labelled-state rules.

### Interactive-asset assessment and gaps

The initial implementation has three original HTML state traces: indexed
arrays, hash buckets, and two pointers. They already supply a labelled initial
state, direct controls, prediction prompt, feedback, scaffold, and transfer
activity. This establishes a useful baseline; it does not establish that
animation itself improves learning.

New work should close these gaps in order:

1. Respect reduced-motion preferences and provide a no-motion direct-step
   route; never require timed playback to perceive a transition.
2. Verify keyboard/focus/screen-reader behavior in a browser, rather than
   testing generated markup alone.
3. Add original semantic visual primitives for binary search, linked rewiring,
   stack/queue state, tree returns, graph frontiers, and DP dependencies.
4. Add constrained learner-input interactions with keyboard equivalents; avoid
   drag-only tasks and keep all input ephemeral.
5. Evaluate unseen transfer and invariant explanations privately and
   optionally. Completion, playback, and time-on-task remain inadequate
   measures of understanding.

OpenDSA is a useful public comparison for paced, input-driven visualizations
and immediate-feedback exercises, but it is not an approved embed or source
asset. Its external runtime and content must not enter this project without a
separate decision. W3C WCAG 2.2 is the accessibility baseline for future
motion behavior; its requirements are implementation constraints, not
pedagogical outcome evidence.

## Core block: 45 minutes

| Segment | Time | Activity | Required output | Tool time |
| --- | ---: | --- | --- | ---: |
| Retrieval opener | 3 min | Answer two related prior-topic prompts without notes. | Answer plus confidence marker. | 0 min |
| Concept model | 7 min | Read one theory paragraph and inspect one labelled visual. | Invariant/contract in own words. | 2 min |
| Worked trace | 7 min | Predict each important state before revealing it. | Trace table or diagram. | 0 min |
| Guided construction | 8 min | Complete scaffolded pseudocode or implementation. | Missing guard, transition, or invariant. | 2 min |
| Contrast | 4 min | Distinguish this method from a close alternative. | “Use X when…; not when…” statement. | 0 min |
| Deliberate practice | 10 min | Complete the pre-code checkpoint, then solve one bounded exercise. | Checkpoint, attempt, complexity, and test cases. | 3 min |
| Feedback and exit | 6 min | Check reasoning, correct one misconception, summarize. | Correction and 2–3 sentence summary. | 1 min |

**Tool-time ceiling: eight minutes.** Opening a problem, executing code,
viewing an animation, or consulting a reference must answer a named question.
No open-ended browsing, solution-video watching, or environment debugging is
allowed during the practice interval. If a tool blocks progress, record the
blocker and continue with pseudocode or a paper trace.

An optional 15-minute extension may add one further exercise or visualization;
it is never required for block completion.

```text
prior cue → predict → concept model → trace → build → contrast
      ↑                                             ↓
later review ← exit summary ← feedback ← problem attempt
```

## Required content elements

### Theory paragraph

Use one paragraph answering: What structure makes the technique relevant? What
state or relationship is maintained? Why is its invariant preserved? What are
the time and auxiliary-space costs? Do not teach several advanced variants in
the same introductory block.

### Visual representation

| Family | Primary visual | Prediction checkpoint |
| --- | --- | --- |
| Arrays, pointers, windows | Indexed array with moving boundaries | Which pointer moves, and why? |
| Hashing | Key/bucket map with collision state | What state exists after this update? |
| Trees and recursion | Call tree or subtree-return diagram | What returns from this node? |
| Graphs | Frontier and visited-set view | Which node enters next? |
| Dynamic programming | State table with dependency arrows | Which earlier states are required? |
| Greedy | Choice timeline and rejected alternatives | What makes this choice safe? |
| Range structures | Interval tree overlay | Which nodes cover this query? |

Keep the label, current state, and explanatory text together. A visual is not a
decoration; it must expose a state relationship that the learner predicts.

### Animation or interactive trace

Use an animation only where state changes: pointer movement, recursion
unwinding, queue expansion, heap repair, union-find compression, or DP filling.
It requires play, pause, step, reset, and a current-state label. Pause before
an important transition and ask for a prediction. Prefer a labelled still image
for static relations such as a complexity contract.

### Questions

Every block has exactly five short prompts:

1. Prior-topic retrieval cue.
2. Invariant/contract prompt before the trace.
3. Next-state prediction during the visual.
4. Contrast question against a nearby technique.
5. Exit question: “What would make this method invalid?”

Answers should require generation, not only recognition. Give concise feedback
after a prediction or at the end of the trace.

### Worked example, scaffold, and transfer

Use a three-stage sequence:

1. **Model:** fully explained tiny example with state and cost.
2. **Completion:** similar input with one missing guard, transition, recurrence,
   or boundary case.
3. **Independent attempt:** new bounded input/problem with no equivalent hint.

The scaffold fades inside the same block. Do not reveal a complete LeetCode
solution before an independent attempt unless the block is explicitly a
post-attempt feedback block.

## Practice design

Select one core exercise by learning target, not merely by topic tag. Prefer a
locally available official-topic LeetCode problem when it has a narrow target;
otherwise use an authored trace or micro-implementation.

| Exercise | Use | Completion evidence |
| --- | --- | --- |
| Trace | New state model/invariant | Correct states and explanation. |
| Micro-implementation | One operation or helper | Normal and boundary tests. |
| LeetCode | Transfer after modelling | Attempt, complexity, learned correction. |
| Contrast | Similar methods, different preconditions | Selection rationale. |

Add only one 2–4 minute prior-topic contrast. For example, contrast a new
sliding-window block with prefix sums, or BFS with DFS order. This interleaves
without turning the block into a broad survey.

## Block authoring template

```markdown
# <Subtopic>

## Target
Recognize <structure> and maintain <invariant/state>.

## Retrieval opener
1. <prior cue>
2. <contrast cue>

## Theory
<structure, invariant, preservation, cost>

## Visual / trace
<diagram specification and prediction checkpoint>

## Worked example
<tiny model input and state changes>

## Faded scaffold
<incomplete trace or pseudocode>

## Independent practice
<one bounded LeetCode/authored exercise; stop rule>

## Feedback checklist
- Invariant stated?
- Boundary case tested?
- Time and auxiliary-space costs named?
- One correction or next adjustment recorded?

## Exit summary
<two to three sentences plus invalid-use condition>
```

## Difficulty and sequence rules

- Establish a stable representation before optimizing it.
- Introduce one new interacting element per block: invariant, data structure, or
  proof idea—not all three.
- Revisit a topic later through retrieval and contrast instead of repeating the
  original explanation.
- Require feedback before moving from a worked trace to independent practice;
  time invested alone does not justify promotion.
- Keep imported problem statements separate from editorial explanations and
  solution feedback under the existing LeetCode-content boundary.

## Implementation acceptance criteria

A block is ready to implement only when it:

- fits the 45-minute schedule and eight-minute tool-time ceiling;
- includes theory, one primary visual, prediction, faded scaffold, independent
  exercise, feedback, and exit summary;
- provides keyboard-accessible play/pause/step/reset controls for any animation;
- presents code, visual state, and feedback sequentially rather than demanding
  simultaneous attention to unrelated panes;
- labels target technique, invariant, expected complexity, and stop rule; and
- records an attempt and feedback separately without creating a mastery score.

## Initial sequence

1. Arrays and indexing contracts.
2. Hash-table lookup and collision reasoning.
3. Two pointers and monotonic movement.
4. Sliding-window invariants, contrasted with prefix sums.
5. Linked-list rewiring and cycle detection.
6. Stack/queue state and monotonic-stack decisions.
7. Binary-search predicates and interval conventions.
8. Tree recursion and subtree return values.
9. BFS/DFS frontier and visited-state choices.
10. Dynamic-programming state, transition, and base cases.

The same block architecture extends to union-find, heaps, tries, shortest
paths, range structures, string matching, greedy proofs, and flow. Any durable
implementation remains an experiment until separately promoted through the
workspace and Registry process.
