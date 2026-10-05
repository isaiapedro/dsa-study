# 13. Flow, matching, and assignment

Flow models limited capacity moving through a network. Matching chooses compatible pairs. Assignment adds a cost or value to each pair.

## 13.1 Capacity and residual edges

A flow network has a source s, a sink t, and directed edges with nonnegative capacities. An edge's flow cannot exceed its capacity. At every other vertex, incoming flow equals outgoing flow.

The residual network describes changes still possible. An edge with capacity 5 and flow 3 allows 2 more units forward and 3 units backward. A backward edge means canceling some earlier flow, not sending a negative physical quantity.

For s → A of capacity 4 and A → t of capacity 3, the path carries at most 3 units. Its residual capacities become 1 and 0 forward, with 3 backward on each used edge. Other outgoing edges from A might allow later rerouting.

Try this: add s → B = 2 and B → t = 2. Complete the total flow and the remaining forward capacities. The value is 5.

Practice: [990. Satisfiability of Equality Equations](https://leetcode.com/problems/satisfiability-of-equality-equations/) is related constraint-modeling practice only. For actual flow conservation, draw the small network above and verify every internal vertex independently.

## 13.2 Augmenting paths and minimum cuts

Ford–Fulkerson repeatedly finds an s-to-t path in the residual network and adds the smallest residual capacity on that path. Include backward residual edges when searching; they allow earlier choices to be repaired.

A cut separates s from t. Its forward capacities bound how much net flow can cross. When no augmenting path remains, let S be the vertices still reachable from s in the residual network. Edges leaving S are saturated and no positive flow enters S that could be canceled backward. The flow value equals the cut capacity, proving both maximum flow and minimum cut.

With integer capacities, each augmentation increases flow by at least one, giving O(EF) time for simple path searches when maximum flow value is F. Arbitrary path choices with irrational capacities need not terminate. Edmonds–Karp chooses shortest residual paths by BFS and guarantees O(VE²), independently of capacity magnitudes.

Try this: saturate one source-to-sink path, then look for a second path that includes a backward edge. Explain which earlier assignment it changes.

Practice: [1349. Maximum Students Taking Exam](https://leetcode.com/problems/maximum-students-taking-exam/) can be approached through bipartite matching and a minimum vertex cover in its conflict graph. Flow is an optional formulation; bitmask DP is another approach.

## 13.3 Maximum bipartite matching

A bipartite graph splits vertices into left and right groups, with edges only across groups. A matching uses each vertex at most once. To express it as flow, add unit-capacity edges from the source to left vertices, from compatible left to right vertices, and from right vertices to the sink.

An augmenting path alternates unused and used matching edges. Flipping their roles increases the number of pairs by one. If L1 can use R1 or R2 and L2 can use only R1, the initial pair L1–R1 can be changed to L1–R2 so L2 can take R1.

A matching is maximum exactly when no augmenting path exists. Comparing it with a larger matching would reveal an alternating component with one more edge from the larger matching. Hopcroft–Karp finds layers and augments along many shortest paths per phase, taking O(E√V).

Try this: add L3 with only R2 to the example. Explain why three matches remain impossible with two right vertices.

Practice: [1820. Maximum Number of Accepted Invitations](https://leetcode.com/problems/maximum-number-of-accepted-invitations/) directly practices bipartite matching; access may require a subscription. The two-left/two-right example remains a complete local exercise.

## 13.4 Stable matching

Stable matching uses preference orders. A pair blocks a matching when both participants prefer each other to their assigned partners. Stability means no blocking pair exists; it does not mean maximum total happiness.

In deferred acceptance, each free proposer approaches the highest-ranked receiver not yet approached. A receiver tentatively keeps the preferred proposal and rejects the rest. Rejected proposers continue down their lists. With n participants on each side and complete strict preferences, at most n² proposals occur.

Why is the final result stable? If a proposer prefers someone else to their final partner, they proposed to that receiver earlier and were rejected. A receiver's tentative partner only improves, so that receiver does not prefer the rejected proposer at the end. Under these assumptions the result favors the proposing side among stable matchings.

Try this: two proposers both prefer R1; R1 prefers P2. Complete the first rejection and P1's next proposal.

Practice: [1583. Count Unhappy Friends](https://leetcode.com/problems/count-unhappy-friends/) exercises blocking-pair detection in a supplied matching. It is not the two-sided deferred-acceptance construction.

## 13.5 Minimum-cost assignment

Assignment pairs every worker with one task while minimizing total cost. Stable matching instead respects preferences, so the objectives can disagree.

For costs [[4, 1], [2, 6]], pairing worker 1 with task 2 and worker 2 with task 1 costs 3; the other assignment costs 10. Exhaustively checking n! assignments soon becomes impractical.

The Hungarian algorithm maintains row and column labels with row_label[i] + column_label[j] ≤ cost[i][j]. Their sum is a lower bound on every complete assignment. Edges meeting equality are tight. Search for an augmenting matching among tight edges; when blocked, adjust labels by the smallest slack crossing the reached/unreached boundary to expose a new tight edge while keeping all inequalities valid. A complete tight matching reaches the lower bound and is therefore optimal. A standard dense implementation takes O(n³).

Try this: choose row minima as initial row labels and zero column labels for the two-by-two matrix. Which edges are already tight?

Practice: [1947. Maximum Compatibility Score Sum](https://leetcode.com/problems/maximum-compatibility-score-sum/). Its small constraints allow subset DP; converting scores to costs gives a separate assignment-algorithm exercise.

## Review

Explain the difference between a residual backward edge, an alternating matching edge, and a blocking preference pair. Later, solve a fresh two-by-two assignment by hand and compare it with its lower bound.
