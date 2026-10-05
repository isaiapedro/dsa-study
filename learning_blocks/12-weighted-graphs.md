# 12. Spanning trees and shortest paths

A minimum spanning tree connects all vertices with the least total edge weight. A shortest-path tree minimizes distance from one chosen source to each reachable vertex. These are different objectives.

## 12.1 Minimum spanning trees

A spanning tree of a connected undirected graph uses V - 1 edges and has no cycle. A cut separates the vertices into two groups. A lightest edge across a cut can safely extend a compatible minimum spanning forest: if an optimal tree omits it, add it, forming a cycle, and remove a crossing edge no lighter than it.

Kruskal's algorithm sorts edges by weight and accepts an edge if its endpoints are in different disjoint sets. It takes O(E log E) time plus near-linear disjoint-set work. Prim's algorithm grows one tree by repeatedly choosing the cheapest edge from its current vertices to a new vertex. An adjacency-list version with a binary heap commonly takes O((V + E) log V).

For edges A–B = 2, B–C = 3, A–C = 8, choose the first two for total 5. Starting at A, the shortest path to C also happens to use them, but this agreement is not guaranteed in other graphs. Negative weights are allowed for MSTs.

Try this: make A–C = 4 and B–C = 3. The MST still totals 5, but A's shortest path to C is the direct weight-4 edge.

Practice: [1584. Min Cost to Connect All Points](https://leetcode.com/problems/min-cost-to-connect-all-points/).

## 12.2 Relaxation and Dijkstra's algorithm

Relaxing edge u → v with weight w means checking whether distance[u] + w improves distance[v]. Distances start at infinity except the source, which starts at zero. Every finite recorded distance represents the cost of a discovered path, so it cannot be below the true shortest distance.

Dijkstra repeatedly settles the reachable unsettled vertex with smallest tentative distance. With nonnegative weights, a path through any later vertex cannot produce a smaller settled distance. That is the reason its greedy step works.

For S → A = 6, S → B = 2, B → A = 1, settle S, then B at 2, then A at 3. A heap implementation may contain an old entry A = 6; discard stale entries. A lazy heap costs O((V + E) log(V + E)); on ordinary simple graphs this is commonly written O((V + E) log V).

Try this: change B → A to -5 and consider a case where A is settled before B. The nonnegative-edge proof no longer applies.

Practice: [743. Network Delay Time](https://leetcode.com/problems/network-delay-time/).

## 12.3 Negative edges, DAG paths, and constraints

Bellman–Ford relaxes every edge repeatedly. After k complete passes, shortest paths using at most k edges have been found. If no reachable negative cycle exists, a shortest simple path uses at most V - 1 edges. A further improvement after those passes signals a reachable negative cycle. Time is O(VE).

A DAG has no cycles at all, so process vertices in topological order and relax each outgoing edge once. Negative weights are safe because dependencies never loop backward. Time is O(V + E).

Difference constraints have the form x_v - x_u ≤ w. Represent each as edge u → v of weight w. Add a source reaching every vertex with zero-weight edges. Shortest distances satisfy the constraints if no negative cycle exists. Summing constraints around a negative cycle would require 0 to be negative, which is impossible.

Try this: combine x_B - x_A ≤ 2 and x_A - x_B ≤ -3. Their sum requires 0 ≤ -1, so there is no solution.

Practice: [787. Cheapest Flights Within K Stops](https://leetcode.com/problems/cheapest-flights-within-k-stops/). Use separate distance arrays per pass to enforce the edge-count limit; ordinary in-place passes may propagate too far.

## 12.4 All-pairs shortest paths

Floyd–Warshall lets intermediate vertices into paths one at a time. Its update is d[i][j] = min(d[i][j], d[i][k] + d[k][j]). Put k in the outer loop so each stage consistently uses only the intermediates introduced so far.

For A → B = 3, B → C = 2, A → C = 9, admitting B improves A → C to 5. Initialize diagonal distances to zero and missing edges to infinity. The algorithm takes O(V³) time and O(V²) space. A negative diagonal after processing signals a negative cycle; ordinary finite shortest-path answers are not valid for pairs that can pass through such a cycle.

Another view uses matrix multiplication with minimum replacing addition and addition replacing multiplication. Combining two path-length matrices joins paths. Repeated squaring increases the allowed number of edges and connects graph optimization to algebra.

Try this: remove B → C. Explain why infinity must not create a fake route, especially in languages with bounded integers.

Practice: [1334. Find the City With the Smallest Number of Neighbors at a Threshold Distance](https://leetcode.com/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance/).

## 12.5 Johnson's reweighting

For a sparse directed graph with negative edges but no negative cycles, Johnson's algorithm first computes vertex potentials h with Bellman–Ford from an added source. Replace each weight by w'(u, v) = w(u, v) + h(u) - h(v). The shortest-distance inequalities make every new weight nonnegative.

Along a path from s to t, all internal potentials cancel, leaving original_cost + h(s) - h(t). Every path between the same endpoints changes by the same amount, so the shortest one stays shortest. Run Dijkstra from each vertex, then undo the endpoint correction.

With binary heaps on a simple graph, the total bound is O(VE + V(V + E) log V), plus storage for any distance matrix retained. It is useful when repeated Dijkstra on the reweighted sparse graph beats cubic work.

Try this: use h(A) = 0, h(B) = -2 on edge A → B of weight -2. The new weight is zero; recovering the original path cost returns -2.

Practice: [743. Network Delay Time](https://leetcode.com/problems/network-delay-time/) practices the Dijkstra stage only. Independently reweight a three-vertex graph with one negative edge to practice Johnson's additional step.

## Review

State the graph conditions required by each algorithm before writing code. Later, build a counterexample showing why an MST and a shortest-path tree can differ.
