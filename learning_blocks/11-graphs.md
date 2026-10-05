# 11. Graph representations and traversal

A graph models objects and connections: cities and roads, tasks and dependencies, or cells and allowed moves. Whether edges have direction or weight changes the questions an algorithm can answer.

## 11.1 Representations and paths

An adjacency list stores each vertex's neighbors. It uses O(V + E) space and visits neighbors efficiently. An adjacency matrix uses O(V²) space and answers whether a particular edge exists in O(1). In an undirected list representation, each ordinary edge appears at both endpoints.

A path follows edges from one vertex to another. A cycle returns to a previously visited vertex along a nonempty closed route. An undirected connected component is a maximal group of mutually reachable vertices. In directed graphs, reachability need not work both ways.

For edges A–B, B–C, and D–E, there are two components. Adding C–D joins them. An isolated vertex is also a component, so counting only vertices mentioned in edges can lose data.

Try this: draw both representations for four vertices and two edges. Which uses less storage as the number of isolated vertices grows?

Practice: [1971. Find if Path Exists in Graph](https://leetcode.com/problems/find-if-path-exists-in-graph/) and [133. Clone Graph](https://leetcode.com/problems/clone-graph/).

## 11.2 Breadth-first search

Breadth-first search, or BFS, uses a queue to visit vertices by increasing number of edges from a starting vertex. Mark a vertex discovered when adding it to the queue, so different neighbors do not repeatedly add it.

Start with distance[source] = 0. When an undiscovered neighbor is reached from u, assign distance[neighbor] = distance[u] + 1 and remember u as its parent. The queue processes all distance-d vertices before distance-(d + 1) vertices. A shorter path would have discovered that neighbor earlier, so the first distance is shortest in an unweighted graph.

For A connected to B and C, and B connected to D, the layers are {A}, {B, C}, {D}. If C also connects to D, D is still enqueued once. Following parent references backward recovers one shortest path.

Try this: add a direct A–D edge. Predict D's new distance before tracing. Time is O(V + E) with adjacency lists and space is O(V).

Practice: [994. Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) and [1091. Shortest Path in Binary Matrix](https://leetcode.com/problems/shortest-path-in-binary-matrix/).

## 11.3 Depth-first search and cycles

Depth-first search, or DFS, follows a branch as far as possible before returning. A recursive call stack or an explicit stack stores unfinished work. It is useful for components, cycle structure, and finishing order; it does not generally find the fewest-edge path.

For directed cycle detection, distinguish unseen vertices, active vertices on the current path, and finished vertices. An edge to an active vertex closes a directed cycle. An edge to a finished vertex does not necessarily do so.

In an undirected graph, the edge back to a node's parent is expected. Exclude that particular parent edge before treating a visited neighbor as a cycle. Parallel edges require edge identities or extra care because two distinct edges can connect the same pair.

Try this: trace A → B → C → A. C reaches active A and proves a cycle. Now replace C → A with A → C and explain the difference.

Practice: [200. Number of Islands](https://leetcode.com/problems/number-of-islands/). Count each cell once. Both BFS and DFS work; recursive DFS may exceed Python's recursion limit on a long path.

## 11.4 Topological order

A topological order puts every directed edge's source before its destination. Such an order exists exactly when the graph has no directed cycle.

Kahn's algorithm counts incoming edges, queues every vertex with zero incoming count, then repeatedly removes one and decreases its neighbors' counts. When a count becomes zero, add that vertex. If fewer than V vertices are removed, a cycle remains. This takes O(V + E).

For dependencies A → C, B → C, C → D, either A or B may come first, but both precede C, and C precedes D. A topological order may not be unique. DFS gives another method: reverse finishing order, after ruling out directed cycles.

Try this: add D → B. Why can the zero-incoming process no longer remove every vertex?

Practice: [207. Course Schedule](https://leetcode.com/problems/course-schedule/) and [210. Course Schedule II](https://leetcode.com/problems/course-schedule-ii/).

## 11.5 Strongly connected components

A strongly connected component of a directed graph is a maximal set in which every vertex can reach every other. Collapsing each such group into one vertex creates a directed acyclic graph.

Kosaraju's method performs DFS to record finishing order, reverses all edges, then starts new DFS searches in decreasing original finishing order. Each second-pass search identifies one component. Finishing order makes the next search start in a component that cannot escape to an unassigned component in the reversed graph. Both passes take O(V + E).

For A → B, B → A, B → C, and C → D, D → C, the components are {A, B} and {C, D}. Reversing edges changes which component can reach the other but does not change membership within either group.

Try this: add D → A. Predict the new component before running either pass.

Practice: [802. Find Eventual Safe States](https://leetcode.com/problems/find-eventual-safe-states/). This is a directed-cycle application; solving it by elimination alone does not practice the two-pass SCC algorithm.

## Review

Choose BFS for an unweighted shortest path, DFS for active-path reasoning, and topological order for dependencies. Later, explain why ordinary connected components are insufficient for directed mutual reachability.
