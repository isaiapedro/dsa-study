# 1. Algorithms and mathematical tools

An algorithm is a finite set of steps for solving a problem. A data structure is a way of arranging information so those steps are easy to perform. To find a name in an unsorted list, you can inspect names one by one. To find a name in a sorted list, you can repeatedly discard half the list.

## 1.1 Inputs, answers, and correctness

An input is the information given to a program. The output is the answer it must produce. Start with a small example: given [8, 3, 6], finding the smallest value must return 3. Returning its position would answer a different question.

A useful way to check a loop is to state something that stays true while it runs. This statement is called an invariant. When finding a minimum, the smallest value seen so far really is the minimum of the part already visited. It is true after the first value. Comparing the next value and keeping the smaller one preserves it. After the last value, it describes the entire array. The loop ends because each step visits a new position.

Try this: after reading 8 and 3, predict what happens when 6 arrives. The minimum remains 3. Complete a scan of [9, 4, 7, 2] yourself; explain each change. Decide what your function does with an empty list before writing it.

Practice: [1480. Running Sum of 1d Array](https://leetcode.com/problems/running-sum-of-1d-array/). Explain what each returned position represents.

## 1.2 Running time and memory

Let n be the number of input items. Reading one array position takes constant time in the usual model: O(1). Reading all positions takes O(n). Comparing every pair takes O(n²). Repeatedly halving a search interval takes O(log n). These describe growth, not seconds.

O gives an upper bound for sufficiently large inputs; Ω gives a lower bound; Θ means both bounds match. A full scan is Θ(n), even though calling it O(n²) would also be a loose upper bound. Best case, worst case, and expected case describe different situations and must be named separately.

For eight items, a scan makes eight visits. For sixteen, it makes sixteen. A two-level loop that visits every ordered pair instead grows from 64 visits to 256. Extra memory counts storage beyond the input: one running total uses O(1); a second list of n totals uses O(n). Output storage can be reported separately.

Try this: a program scans n values and then sorts them in O(n log n). Which part controls the growth? Sorting does. Two consecutive scans are O(n), not O(n²).

Practice: [217. Contains Duplicate](https://leetcode.com/problems/contains-duplicate/). Compare checking pairs, sorting, and keeping a set.

## 1.3 Sums, logarithms, and counting

A summation is repeated addition written compactly. The sum 1 + 2 + ... + n equals n(n + 1)/2. Pair the first and last terms: each pair totals n + 1. This explains why insertion sort can do quadratic work.

The geometric sum 1 + 2 + 4 + ... + 2^k equals 2^(k+1) - 1. Each new term doubles. The reverse process explains logarithms: log₂ n counts how many halvings reduce n to 1. Changing the logarithm's base changes only a constant factor.

A permutation orders all items; a combination chooses items without caring about order. Three distinct items have 3! = 6 arrangements and 2³ = 8 subsets. Choosing two of n distinct items gives n(n - 1)/2 possibilities. These counts often tell you whether exhaustive search can finish.

Try this: count the comparisons needed to compare every unordered pair among five values. There are 5 × 4 / 2 = 10. Complete the same count for six values before checking by enumeration.

Practice: [77. Combinations](https://leetcode.com/problems/combinations/) and [78. Subsets](https://leetcode.com/problems/subsets/). Predict output size before coding.

## 1.4 Sets, relations, functions, graphs, and trees

A set contains distinct items. The union of {2, 5} and {5, 9} is {2, 5, 9}; their intersection is {5}. A relation describes which pairs are connected. Equality is reflexive, symmetric, and transitive. A relation with those three properties partitions items into nonoverlapping groups.

A function assigns each input exactly one output. Different inputs may share an output: a hash function can send two keys to the same bucket. One-to-one functions forbid that sharing; onto functions reach every element of their stated output set.

A graph contains vertices and edges. A tree is a connected undirected graph without cycles. A tree with n vertices has n - 1 edges. Rooting a tree gives each nonroot vertex one parent; its children begin smaller subtrees.

Try this: connect A to B and B to C. Adding A–C creates a cycle. Adding a new vertex D with edge C–D preserves a tree. Explain why each addition has a different effect.

Practice: [349. Intersection of Two Arrays](https://leetcode.com/problems/intersection-of-two-arrays/) and [1971. Find if Path Exists in Graph](https://leetcode.com/problems/find-if-path-exists-in-graph/).

## 1.5 Probability and matrices

A probability lies between 0 and 1. For equally likely outcomes, divide favorable outcomes by all outcomes. Two independent fair coin tosses have outcomes HH, HT, TH, TT; exactly one head has probability 1/2.

A random variable assigns a number to each outcome. Its expectation is a probability-weighted average. An indicator is 1 when an event happens and 0 otherwise, so its expectation is the event's probability. Expectations add even when variables are dependent. Independence is needed for multiplying event probabilities. In independent trials with success probability p, the number of successes in n trials has mean np; the waiting time to the first success has mean 1/p. Tail bounds estimate how unlikely a large departure from the mean is. For any nonnegative X, Markov's bound gives P(X ≥ a) ≤ E[X]/a; stronger binomial bounds use independence.

A matrix is a rectangular table of numbers. Its transpose swaps rows and columns. Multiplication combines a row from the first matrix with a column from the second. The row [2, 1] and column [3, 4] produce 2×3 + 1×4 = 10. The inside dimensions must agree.

Try this: complete [1, 3] · [4, 2] = __. The answer is 10. Explain why multiplying a 2×3 matrix by a 2×2 matrix is undefined.

Practice: [867. Transpose Matrix](https://leetcode.com/problems/transpose-matrix/). For probability, [528. Random Pick with Weight](https://leetcode.com/problems/random-pick-with-weight/) applies cumulative probability.

## 1.6 Programs and data abstraction

A variable names a value. A condition chooses a branch, a loop repeats work, and a function groups steps that produce an answer. Separate a function's inputs and returned value from printing: displaying 3 does not make a caller receive 3 as its result. Check examples before timing a program; a fast wrong answer is still wrong.

A data type describes values and allowed operations. A stack offers push, pop, and an empty check. Its caller need not know whether items live in a linked list or a resizable array. Hiding that representation is data abstraction. The implementation must still preserve the promised behavior, including what happens on an empty pop.

Two names can refer to the same mutable object. If b refers to the same list as a, changing b changes what a observes too. Copying the list separates its outer container, but references to nested mutable objects may still be shared. Immutability avoids this kind of change through an alias.

An API is the set of operations a component exposes. A bag accepts items without promising a removal order; a stack and queue promise different orders. Iteration visits the stored items, but its order depends on the type. Benchmark repeated, representative inputs and report conditions; measured seconds complement a growth analysis rather than proving it.

Try this: let a and b refer to one list [2, 6]. Append 9 through b. Predict what a contains, then compare with making an independent copy first.

Practice: [155. Min Stack](https://leetcode.com/problems/min-stack/). Define the allowed operations and their answers before choosing the internal representation.

## Review

Without notes, explain why a minimum scan is correct, why a triangular loop is quadratic, and why expectation differs from a worst-case guarantee. Revisit these questions in a later session using different numbers.
