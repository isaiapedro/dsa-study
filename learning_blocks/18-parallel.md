# 18. Parallel algorithms and simulation

Parallelism performs independent work at the same time. Event-driven simulation instead skips periods when nothing changes. Both improve performance by examining the dependencies between steps.

## 18.1 Work and span

Work, written T₁, is the total time if one processor performs all operations. Span, written T∞, is the length of the longest dependency chain, assuming unlimited processors. With P processors, execution time is at least max(T₁/P, T∞).

A fork creates independent subtasks and a join waits for their results. Summing n numbers with a balanced reduction tree does O(n) additions and has O(log n) span. A sequential left-to-right sum has the same work but O(n) span.

Under a suitable ideal greedy scheduler, time is bounded on the order of T₁/P + T∞. Real machines also pay for scheduling, communication, and memory access. Work divided by span describes available parallelism; adding processors beyond that scale cannot remove the critical dependency chain.

Try this: a job has work 100 and span 20. With ten processors, its time is at least 20, not 10.

Practice: [1114. Print in Order](https://leetcode.com/problems/print-in-order/) practices ordering between concurrent tasks. Work/span analysis needs the separate arithmetic example above.

## 18.2 Parallel matrix multiplication

Different output entries of a matrix product are independent if each task writes its own entry. Within an entry, the dot-product terms can be summed with a tree reduction. For dense n×n matrices, straightforward arithmetic work is O(n³), while ideal dot-product reduction depth is O(log n), with additional task-spawning depth in a bounded-fan-out model.

Avoid races: two tasks must not update the same sum without coordination. One approach gives each task a private partial result, then combines partials in a defined reduction. Keeping every partial simultaneously can use substantial memory, so practical designs limit task size and reuse storage.

Block multiplication improves locality by reusing pieces already near the processor. A theoretically smaller span does not imply less memory traffic or faster elapsed time.

Try this: assign the four entries of a two-by-two product to four tasks. Which values are shared read-only, and which outputs have a single writer?

Practice: [48. Rotate Image](https://leetcode.com/problems/rotate-image/) is related matrix-index practice only. The actual parallel exercise is to draw the four-task dependency graph and identify a deliberately unsafe shared accumulator.

## 18.3 Parallel sorting and synchronization

Parallel mergesort sorts two halves concurrently, then merges them. If merging stays sequential, the span obeys S(n) = S(n/2) + O(n), giving O(n), even though the recursive calls run together.

To merge in parallel, choose a midpoint in the larger sorted half, binary-search its rank in the other half, and place it in its final output position. The values before and after it form independent smaller merges. A balanced implementation has O(n) merge work and O(log² n) merge span, yielding O(n log n) sorting work and O(log³ n) span for this version.

Disjoint output ranges prevent writes from colliding. A join must occur before a parent reads the sorted outputs of its children. Deterministic ordering of equal keys needs an explicit tie rule if stability is required.

Try this: split a merge of [1, 5, 9] and [2, 6] around 5. Its final index is 2, and the remaining output ranges lie on opposite sides.

Practice: [88. Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/) practices merging. Use a separate scratch output array for the parallel split exercise; in-place writes introduce additional dependencies.

## 18.4 Event-driven simulation

A time-step simulation updates the world at every small interval. An event-driven simulation stores future changes in a priority queue and jumps directly to the earliest event.

For moving particles, a predicted collision depends on positions and velocities. If another collision changes a particle's velocity first, the old prediction becomes invalid. Attach a version or collision count to each prediction and discard it when the participating particles' versions no longer match.

For particles at x = 0 and x = 10 moving toward each other at speeds 2 and 3, point-particle collision occurs after 10/(2 + 3) = 2 time units. Finite radii reduce the gap between surfaces. After handling the collision, update the affected motion and predict new events.

A heap with Q entries takes O(log Q) per insertion or removal, but total runtime also includes prediction work and invalidated events. Simultaneous events need a consistent physical or discrete model.

Try this: add a wall collision that changes the first particle's direction at time 1. Explain why the old time-2 collision prediction must be discarded.

Practice: [1834. Single-Threaded CPU](https://leetcode.com/problems/single-threaded-cpu/) practices event ordering and priority queues, not particle physics.

## Review

Explain the difference between total work and the longest chain of dependent work. Later, trace one stale event and one unsafe shared write and show how each is prevented.
