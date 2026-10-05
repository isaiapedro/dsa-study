- [x] ss# DSA Research Queries

Search queries for locating objective research papers and surveys relevant to
the DSA Study curriculum. Use scholarly indexes such as Google Scholar,
Semantic Scholar, ACM Digital Library, IEEE Xplore, or arXiv. These queries do
not direct the storage of external material; see `CURRICULUM.md` and
`DECISIONS.md` for the link-only source policy.

## Algorithmic foundations

| Priority | Topic                                           | Search query                                                                        |
| -------- | ----------------------------------------------- | ----------------------------------------------------------------------------------- |
| 1        | Algorithm analysis, correctness, and invariants | `"algorithm correctness" loop invariants proof pedagogy computer science education` |
| 2        | Amortized analysis and dynamic data structures  | `"amortized analysis" dynamic data structures survey`                               |
| 3        | Hashing and randomized algorithms               | `"universal hashing" randomized algorithms survey expected time`                    |
| 4        | Union-find / disjoint sets                      | `Tarjan union-find path compression union by rank analysis`                         |
| 5        | Dynamic programming                             | `"dynamic programming" algorithm design pedagogy systematic review`                 |
| 6        | Greedy algorithms and proof techniques          | `"greedy algorithms" exchange argument proof pedagogy`                              |

## Data structures and graph algorithms

| Priority | Topic                     | Search query                                                           |
| -------- | ------------------------- | ---------------------------------------------------------------------- |
| 7        | Shortest-path algorithms  | `"shortest path algorithms" survey Dijkstra Bellman-Ford A star`       |
| 8        | Network flow and matching | `"maximum flow" "bipartite matching" algorithms survey`                |
| 9        | Range-query structures    | `"range query data structures" segment tree Fenwick tree survey`       |
| 10       | String algorithms         | `"string matching algorithms" survey KMP Aho-Corasick suffix array`    |
| 11       | Dynamic graph structure   | `"dynamic graph algorithms" connectivity minimum spanning tree survey` |

## Evidence for study-system design

| Priority | Topic                                       | Search query                                                                                 |
| -------- | ------------------------------------------- | -------------------------------------------------------------------------------------------- |
| 12       | Adaptive problem sequencing                 | `"programming problem recommendation" learner modeling data structures algorithms education` |
| 13       | Worked examples for novice learners         | `"worked example effect" programming education algorithm learning`                           |
| 14       | Retrieval practice in programming education | `"retrieval practice" programming education computer science`                                |
| 15       | Interleaved algorithm practice              | `interleaving practice algorithm learning computer science education`                        |

## Suggested first batch

Start with queries 1–7 and 12–15. Together they address the main missing
evidence: rigorous algorithmic foundations and research supporting the
project's future review and sequencing features.

## Interactive learning, accessibility, and evaluation gaps

| Priority | Topic | Search query | Reason |
| --- | --- | --- | --- |
| 16 | Algorithm-visualization engagement | `"algorithm visualization" engagement prediction feedback systematic review` | Distinguish learner-controlled prediction and feedback from passive animation. |
| 17 | DSA pedagogy evidence | `"teaching algorithm design" literature review undergraduate evaluation` | Find topic-specific evidence and identify gaps rather than extrapolating general learning studies. |
| 18 | Accessible interactive diagrams | `WCAG 2.2 animation from interactions prefers-reduced-motion keyboard interactive visualization` | Verify no-motion, keyboard, and text-equivalent requirements before new visual primitives. |
| 19 | Interactive DSA assets | `OpenDSA algorithm visualization proficiency exercise open source license accessibility` | Evaluate external comparison assets without assuming that they may be embedded or copied. |
| 20 | Transfer assessment | `algorithm education transfer assessment invariant explanation debugging study` | Design a private, low-stakes evaluation that measures reasoning rather than completion. |

### Reviewed references, 2026-09-11

- [W3C: Animation from Interactions](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html) and [Pause, Stop, Hide](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html): motion must be controllable or avoidable where non-essential; they inform accessibility requirements, not learner-effect claims.
- [Hundhausen, Douglas, and Stasko (2002)](https://users.cs.duke.edu/~rodger/jflappapers/Hundhausen2002.pdf), *A Meta-Study of Algorithm Visualization Effectiveness*: supports treating engagement as material and does not justify passive animation as sufficient.
- [Liu et al. (2024)](https://arxiv.org/abs/2405.00832), *Teaching Algorithm Design: A Literature Review*: reports sparse, uneven topic-specific evaluation evidence; it motivates project evaluation rather than a general learning claim.
- [OpenDSA](https://opendsa.org/home/about): a public comparison source for paced visualizations, constrained input, exercises, and feedback. It is not an approved dependency, embed, or content source for this project.

### Research completion, 2026-09-11

All query groups have a governed local record, a link-only source, or a
documented evidence limitation in [RESEARCH_SYNTHESIS.md](RESEARCH_SYNTHESIS.md).
Recent primary additions cover [loop-invariant learning](https://par.nsf.gov/biblio/10195158-learning-loop-invariants),
[dynamic-programming worked examples](https://doi.org/10.1145/3545947.3576232),
and current [W3C motion guidance](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html).
The transfer rubric is intentionally an unvalidated, private reflection design;
no query result supports using it for mastery, interview, or hiring claims.
