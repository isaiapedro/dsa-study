# Course sequence

Read modules in the order in [CURRICULUM.md](CURRICULUM.md), or use the prerequisites below to revisit a topic. A module contains several short sections and can take several sessions.

| Module | Earlier ideas to know |
| --- | --- |
| [1. Algorithms and mathematical tools](learning_blocks/01-foundations.md) | Basic reading of numbers and short programs |
| [2. Arrays, lists, stacks, and queues](learning_blocks/02-arrays.md) | 1. Algorithms and mathematical tools |
| [3. Searching arrays and using windows](learning_blocks/03-searching.md) | 1. Algorithms and mathematical tools; 2. Arrays, lists, stacks, and queues |
| [4. Sorting and selecting](learning_blocks/04-sorting.md) | 1. Algorithms and mathematical tools; 2. Arrays, lists, stacks, and queues; 3. Searching arrays and using windows |
| [5. Recursion, randomness, and amortized cost](learning_blocks/05-analysis.md) | 1. Algorithms and mathematical tools; 4. Sorting and selecting |
| [6. Hash tables and symbol tables](learning_blocks/06-hashing.md) | 1. Algorithms and mathematical tools; 2. Arrays, lists, stacks, and queues; 5. Recursion, randomness, and amortized cost |
| [7. Search trees and larger indexes](learning_blocks/07-trees.md) | 2. Arrays, lists, stacks, and queues; 5. Recursion, randomness, and amortized cost; 6. Hash tables and symbol tables |
| [8. Disjoint sets and range queries](learning_blocks/08-union-find.md) | 2. Arrays, lists, stacks, and queues; 5. Recursion, randomness, and amortized cost; 7. Search trees and larger indexes |
| [9. Dynamic programming](learning_blocks/09-dynamic-programming.md) | 1. Algorithms and mathematical tools; 2. Arrays, lists, stacks, and queues; 5. Recursion, randomness, and amortized cost |
| [10. Greedy choices and online decisions](learning_blocks/10-greedy.md) | 4. Sorting and selecting; 5. Recursion, randomness, and amortized cost; 6. Hash tables and symbol tables; 9. Dynamic programming |
| [11. Graph representations and traversal](learning_blocks/11-graphs.md) | 2. Arrays, lists, stacks, and queues; 8. Disjoint sets and range queries |
| [12. Spanning trees and shortest paths](learning_blocks/12-weighted-graphs.md) | 4. Sorting and selecting; 8. Disjoint sets and range queries; 11. Graph representations and traversal |
| [13. Flow, matching, and assignment](learning_blocks/13-flow.md) | 9. Dynamic programming; 11. Graph representations and traversal; 12. Spanning trees and shortest paths |
| [14. String sorting, tries, and matching](learning_blocks/14-strings.md) | 3. Searching arrays and using windows; 4. Sorting and selecting; 6. Hash tables and symbol tables; 7. Search trees and larger indexes |
| [15. Regular expressions and compression](learning_blocks/15-compression.md) | 10. Greedy choices and online decisions; 11. Graph representations and traversal; 14. String sorting, tries, and matching |
| [16. Matrices, linear programming, and FFT](learning_blocks/16-numerical.md) | 1. Algorithms and mathematical tools; 5. Recursion, randomness, and amortized cost; 9. Dynamic programming |
| [17. Number theory and bit operations](learning_blocks/17-number-theory.md) | 1. Algorithms and mathematical tools; 5. Recursion, randomness, and amortized cost |
| [18. Parallel algorithms and simulation](learning_blocks/18-parallel.md) | 2. Arrays, lists, stacks, and queues; 4. Sorting and selecting; 5. Recursion, randomness, and amortized cost; 16. Matrices, linear programming, and FFT |
| [19. Clustering, weights, and gradient descent](learning_blocks/19-learning.md) | 1. Algorithms and mathematical tools; 5. Recursion, randomness, and amortized cost; 16. Matrices, linear programming, and FFT |
| [20. Hard problems and approximation](learning_blocks/20-hard-problems.md) | 5. Recursion, randomness, and amortized cost; 9. Dynamic programming; 10. Greedy choices and online decisions; 11. Graph representations and traversal; 13. Flow, matching, and assignment |

## Interactive examples

The nine examples in blocks.json reinforce sections of the written course.

| Example ID | Course module |
| --- | --- |
| arrays-indexing-contracts | [Arrays and positions](learning_blocks/02-arrays.md) |
| hashing-collision-reasoning | [Hash tables and collisions](learning_blocks/06-hashing.md) |
| two-pointers-monotonic-movement | [Two pointers in a sorted array](learning_blocks/03-searching.md) |
| binary-search-interval-invariant | [Binary search](learning_blocks/03-searching.md) |
| linked-lists-rewiring-contracts | [Changing linked-list connections](learning_blocks/02-arrays.md) |
| stacks-queues-order-contracts | [Stacks and queues](learning_blocks/02-arrays.md) |
| trees-recursive-return-contracts | [Recursion on trees](learning_blocks/07-trees.md) |
| bfs-dfs-frontier-visited-contracts | [Breadth-first and depth-first search](learning_blocks/11-graphs.md) |
| dynamic-programming-dependency-contracts | [Building a dynamic-programming table](learning_blocks/09-dynamic-programming.md) |

The course map is fixed authored navigation. It does not read progress or infer readiness. The written chapters are the complete topic map; the nine interactive examples are a smaller practice collection.
