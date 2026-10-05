# 8. Disjoint sets and range queries

Some structures answer specialized questions very efficiently. Disjoint sets track which items belong together. Range structures combine values over intervals.

## 8.1 Disjoint-set operations

A disjoint-set structure, also called union-find, partitions items into nonoverlapping groups. make_set creates a one-item group, find returns its representative, and union combines two groups.

For {A}, {B}, {C}, union(A, B) produces {A, B}, {C}. After union(B, C), all three have the same representative. Its identity is an implementation detail; equal representatives mean connected groups.

A simple linked-list representation keeps members together and stores a representative reference for each. Union can relabel every member of the smaller list and append it to the larger. Each time an item is relabeled, its group at least doubles, so each item is relabeled at most O(log n) times. Total relabeling over all unions is O(n log n).

A forest representation instead makes each representative a root. Parent references lead from each member toward that root, so union can link roots instead of relabeling every member.

Try this: perform union(0, 2), union(1, 3), union(2, 3). Predict whether find(0) and find(1) agree.

Practice: [547. Number of Provinces](https://leetcode.com/problems/number-of-provinces/).

## 8.2 Path compression and union by size

Union by size attaches the smaller root below the larger root. Without compression, a node's depth increases only when its component at least doubles, so depth is O(log n). Union by rank uses a height-related upper bound instead of an exact size.

Path compression shortens paths during find by making visited nodes point toward the root. If 5 → 3 → 1, finding 5 can change it directly to 5 → 1. Together with union by rank or size, a sequence of operations has an amortized inverse-Ackermann cost, usually written O(α(n)) per operation after accounting for initialization. It grows extraordinarily slowly, but this is a sequence bound, not literal constant worst-case time.

The analysis groups nodes by increasing rank ranges: parent ranks rise along paths, and compression prevents repeatedly traversing the same long low-rank portions without progress. The formal accounting yields α(n); the useful programming lesson is to use both balancing and compression.

Try this: union two equal-size groups, then compress a member's path. Why must future unions still compare roots?

Practice: [684. Redundant Connection](https://leetcode.com/problems/redundant-connection/). Ordinary union-find supports adding connectivity; deleting an edge may split a group and requires a different approach.

## 8.3 Prefix sums and Fenwick trees

Prefix sums answer static interval sums quickly, but changing one array value changes many later prefixes. A Fenwick tree stores partial sums for carefully chosen ranges so a point update and a prefix query both take O(log n).

Use one-based indices. lowbit(i) = i & -i isolates the lowest set bit. tree[i] stores the lowbit(i) positions ending at i. Thus tree[6] covers positions 5–6 and tree[4] covers 1–4. A prefix query for 6 adds those two entries by repeatedly subtracting lowbit(i).

An update at position 3 visits 3, 4, 8, and so on by adding lowbit(i), updating every stored range containing that position. To assign a new value, update by the difference between new and old values.

Try this: complete a prefix query for index 7. It visits 7, 6, 4, then stops at 0. Explain why the ranges do not overlap.

Practice: [307. Range Sum Query - Mutable](https://leetcode.com/problems/range-sum-query-mutable/).

## 8.4 Segment trees and sparse tables

A segment tree recursively splits an interval and stores a summary at each node. A sum node stores the sum of its two children. A minimum node stores their minimum. Queries combine the nodes that exactly cover the requested interval.

For [2, 7, 1, 4], the root sum is 14 and its children store 9 and 5. Updating the 7 to 3 changes its leaf, the left child to 5, and the root to 10. Only O(log n) ancestors change. Building takes O(n) time and storage; range queries and point updates take O(log n).

Lazy propagation supports certain range updates by saving a pending update on a whole covered node. For range addition and sum, adding d to a segment of length L increases its sum by dL. Push pending updates before inspecting children. The update-combination rule must match the operation.

A sparse table instead precomputes intervals of power-of-two lengths for static data. Minimum queries can combine two overlapping intervals in O(1), because repeating a value does not change a minimum. Ordinary sums cannot use that overlapping trick.

Try this: explain why min(2, 2, 7) equals min(2, 7), while the sums differ.

Practice: [307. Range Sum Query - Mutable](https://leetcode.com/problems/range-sum-query-mutable/) and [315. Count of Smaller Numbers After Self](https://leetcode.com/problems/count-of-smaller-numbers-after-self/).

## Review

Choose among prefix sums, a Fenwick tree, and a segment tree by naming the needed queries and updates. Later, explain why union-find cannot simply undo an arbitrary deleted edge.
