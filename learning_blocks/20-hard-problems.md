# 20. Hard problems and approximation

Some problems have no known polynomial-time algorithm. We can still solve small instances exactly, exploit special structure, or accept an answer with a proved approximation bound.

## 20.1 Polynomial time, verification, and reductions

A decision problem asks a yes/no question. P contains decision problems solvable in polynomial time. NP contains decision problems whose yes answers have certificates verifiable in polynomial time. Every problem in P is in NP; whether P equals NP is unknown.

A Hamiltonian-cycle certificate lists a cycle visiting every vertex once. Checking its edges and coverage is easy even though finding one may be difficult. NP does not mean “non-polynomial”; it describes verification.

A polynomial-time reduction transforms instances of problem A into instances of problem B while preserving yes/no answers. An efficient solver for B would then solve A. To show B is hard, reduce a known hard A to B, not the reverse. NP-complete means both in NP and at least as hard as every problem in NP under the chosen polynomial reductions.

A common proof chain passes through Boolean circuit satisfiability, Boolean satisfiability, 3-CNF satisfiability, clique, vertex cover, Hamiltonian cycle, traveling salesperson decision, and subset sum. Each link needs a construction in polynomial time and a proof in both directions. Complementing a graph connects a clique of size k with an independent set of size k; the complement of a vertex cover is an independent set.

Try this: if A reduces to B and B has a fast algorithm, which problem also becomes fast? A does.

Practice: [785. Is Graph Bipartite?](https://leetcode.com/problems/is-graph-bipartite/) supplies a tractable graph decision problem to contrast with general graph coloring. It does not prove NP-completeness.

## 20.2 Backtracking and exact exponential algorithms

Backtracking explores a tree of decisions. At each node, choose an option, update the partial solution, recurse, then undo the choice. Prune a branch only when it cannot lead to a valid or better answer.

For subsets of [2, 5, 7], each level chooses whether to include one value. There are 2³ leaves. If all remaining values are positive and the current sum already exceeds a target, no extension can repair it. That pruning argument fails when negative values are allowed.

For n-queens, keep occupied columns and diagonals. A candidate square conflicting with an earlier queen can be rejected immediately. The checks avoid many branches but do not convert the general search into a polynomial-time algorithm.

Dynamic programming over subsets stores an answer for each visited set and endpoint, often reducing a factorial search to O(n²2^n), as in a standard exact traveling-salesperson recurrence. It remains exponential. Output size can also force exponential time when the task asks for every subset or permutation.

Try this: trace include/exclude choices until finding sum 7 from [2, 5, 7]. Identify both solutions and explain which branches can be pruned.

Practice: [51. N-Queens](https://leetcode.com/problems/n-queens/) and [698. Partition to K Equal Sum Subsets](https://leetcode.com/problems/partition-to-k-equal-sum-subsets/).

## 20.3 Vertex cover and metric traveling salesperson

An approximation algorithm has a proved relationship to the best answer. For a minimization problem, a factor-r algorithm returns cost at most r times optimum. A heuristic without such a proof may work well but has a different guarantee.

For vertex cover in an undirected graph, repeatedly choose an uncovered edge and put both endpoints into the cover. The chosen edges share no endpoints, so any cover must choose at least one endpoint from each. Taking two per chosen edge gives a factor-2 approximation. The cover is valid because the process stops only after every edge has a selected endpoint.

For symmetric metric traveling salesperson, distances satisfy the triangle inequality. Build an MST, double its edges to obtain a closed walk, then shortcut repeated vertices. The MST costs no more than an optimal tour; doubling gives at most twice that cost, and shortcutting cannot increase it. Without the triangle inequality, the shortcut argument fails.

Try this: apply the cover rule to path A–B–C–D. If you first choose B–C, the cover {B, C} covers every edge.

Practice: [847. Shortest Path Visiting All Nodes](https://leetcode.com/problems/shortest-path-visiting-all-nodes/) is related exact state-space search, not the metric-tour approximation. Trace the doubled-MST tour separately.

## 20.4 Set cover, linear relaxations, and random choices

Set cover chooses sets whose union contains every required element. In unweighted greedy set cover, repeatedly take the set covering the most uncovered elements. For universe size U, the usual guarantee is H_U, the harmonic sum, and therefore at most 1 + ln U.

The charging argument divides each chosen set's cost among the new elements it covers. Compare those charges with an optimal set: as its uncovered elements disappear, their charges are bounded by successive reciprocal counts. Summing gives the harmonic factor. Weighted cover chooses the smallest cost per newly covered element instead.

Linear programming can relax a yes/no choice into a fraction between 0 and 1, producing a bound on the integer optimum. For vertex cover, minimize Σx_v subject to x_u + x_v ≥ 1 on every edge. Rounding every x_v ≥ 1/2 upward covers every edge and costs at most twice the relaxed optimum.

Randomization can also provide an expected guarantee. Independently assigning Boolean variables makes a nonempty clause with at most three distinct literals true with probability at least 1/2; with exactly three distinct variables it is 7/8. Adding clause indicators bounds expected satisfied clauses. This is an expectation, not a guarantee for every run.

Try this: for universe {a,b,c,d}, compare sets {a,b,c}, {c,d}, and {d}. Complete greedy cover in two steps.

Practice: [1125. Smallest Sufficient Team](https://leetcode.com/problems/smallest-sufficient-team/) directly models set cover, but its small skill universe permits exact subset DP.

## 20.5 Subset sum and approximation schemes

Subset sum asks whether some subset reaches a target. A dynamic program over sums 0 through T takes O(nT), which is polynomial in numeric T but not in its input length log T. This is called pseudopolynomial time.

For maximizing a subset sum not exceeding T, maintain attainable sums. For each positive item, merge the old list with a shifted copy and discard sums above T. The exact list can grow exponentially.

An approximation scheme trims nearly equal sums: retain a smaller representative and discard slightly larger values that it approximates within a chosen multiplicative factor. The smaller representative stays feasible for future additions. If one round loses at most a factor 1 + δ, after n rounds the loss is at most (1 + δ)^n. Choose δ in terms of ε/n to keep the total error within the desired bound.

For the standard positive-integer formulation, trimming yields a fully polynomial-time approximation scheme: runtime is polynomial in input size and 1/ε. Smaller ε means greater accuracy and more work. The guarantee concerns the optimization version, not an exact yes/no answer about reaching T.

Try this: with limit 10 and values [4, 6, 7], list the attainable feasible sums after each item. Explain why discarding a sum above 10 is safe only under the nonnegative-input assumption.

Practice: [416. Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/) practices exact sum DP. Implement trimming separately and compare its answer with exact enumeration on small original inputs.

## Review

Explain the direction of a reduction, the meaning of a factor-2 guarantee, and why O(nT) may fail to be polynomial in input length. Later, compare exact DP, backtracking, and approximation on one small subset-sum instance.
