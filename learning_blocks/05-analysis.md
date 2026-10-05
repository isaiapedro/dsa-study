# 5. Recursion, randomness, and amortized cost

Three different questions need three different tools: how recursive work grows, how random choices affect expected work, and how expensive operations spread across a sequence.

## 5.1 Recursive calls and divide and conquer

A recursive function solves a smaller version of its own problem. It needs a base case and a step that moves toward it. To total a tree, return zero for an absent node and otherwise combine the node's value with the totals of its children.

Divide and conquer solves several smaller problems and combines their answers. Mergesort's halves are independent; dynamic programming becomes useful when recursive calls repeatedly solve the same subproblem.

A recurrence describes total work. For mergesort, T(n) = 2T(n/2) + Θ(n). The two recursive calls sort the halves; the final term pays for splitting and merging. For binary search with constant-time indexing, T(n) = T(n/2) + Θ(1). Copying slices at every search step changes that cost.

Try this: draw the calls for summing a root with two leaf children. Each node contributes once, so time is O(n); the active calls follow one root-to-leaf path, using O(h) space.

Practice: [104. Maximum Depth of Binary Tree](https://leetcode.com/problems/maximum-depth-of-binary-tree/).

## 5.2 Solving recurrences

A recursion tree puts work at each depth on one row. For T(n) = 2T(n/2) + n, the root costs n, the next row has two costs of n/2, and each later row also totals n. O(log n) rows give O(n log n).

Substitution proves a proposed bound by induction. Guess a bound, substitute it into the recurrence, and choose constants that make the inequality hold, including the small base cases. A plausible-looking tree is useful intuition; induction checks the claim.

The master method summarizes common recurrences T(n) = aT(n/b) + f(n). Compare f(n) with n^(log_b a). Polynomially smaller extra work gives Θ(n^(log_b a)); equal-order work gives Θ(n^(log_b a) log n); polynomially larger work gives Θ(f(n)) when the usual regularity condition holds.

Unequal splits need another tool. Akra–Bazzi, under its regularity conditions, uses a value p satisfying Σ a_i b_i^p = 1 for subproblem fractions b_i, and gives Θ(n^p(1 + ∫₁ⁿ g(u)/u^(p+1) du)). For T(n) = T(n/3) + T(2n/3) + n, p = 1, giving Θ(n log n). The integral expresses the same accumulation of work across scales as a recursion tree.

Try this: complete the rows for T(n) = 4T(n/2) + n. Leaf growth dominates, giving Θ(n²).

Practice: [241. Different Ways to Add Parentheses](https://leetcode.com/problems/different-ways-to-add-parentheses/). Count repeated subproblems; this is related recursion practice, not a master-method exercise.

## 5.3 Randomized algorithms and expected cost

Randomized algorithms deliberately use random choices. Randomized quicksort chooses pivots independently of input order. Probabilistic input analysis instead assumes a distribution of inputs. These are different sources of randomness.

Imagine interviewing n candidates in random order and selecting a candidate whenever they are better than everyone seen so far. Candidate i is best among the first i with probability 1/i. Add indicator expectations: the expected number of selections is 1 + 1/2 + ... + 1/n = Θ(log n). This does not say every order makes only logarithmically many selections.

To shuffle uniformly, at step i choose uniformly among the remaining positions and exchange one into position i. Each permutation then has probability 1/n!. For reservoir sampling one item from a stream, replace the saved item at position i with probability 1/i. An earlier item survives with the complementary probabilities, leaving every position equally likely at the end.

Try this: after three stream items, calculate the chance the first remains: 1 × 1/2 × 2/3 = 1/3.

Practice: [384. Shuffle an Array](https://leetcode.com/problems/shuffle-an-array/) and [398. Random Pick Index](https://leetcode.com/problems/random-pick-index/).

## 5.4 Amortized analysis

Amortized cost concerns an entire sequence and does not require randomness. A dynamic array can double its capacity when full. Across n appends, copying costs form a geometric sum: 1 + 2 + 4 + ... < 2n. Adding the n new writes still gives O(n) total work, or O(1) amortized work per append.

Aggregate analysis sums the actual work. The accounting method imagines charging a small extra amount on cheap operations to pay for later expensive ones. The potential method assigns stored credit Φ to the current state and charges actual_cost + Φ_after - Φ_before. The potential terms cancel when summed.

A binary counter provides another example. Incrementing 0111 flips four bits, but the lowest bit flips every time, the next every second time, and so on. Over n increments from zero, fewer than 2n flips occur.

Try this: trace capacities 1, 2, 4, 8 while appending five items. Separate the expensive fifth append from the average over all five. Shrinking storage needs a lower threshold than growth to avoid repeated grow/shrink copies.

Practice: [901. Online Stock Span](https://leetcode.com/problems/online-stock-span/) and [232. Implement Queue using Stacks](https://leetcode.com/problems/implement-queue-using-stacks/). Count how often each item can move or leave a stack.

## 5.5 Bounding random events

Indicator variables let you count events without listing all combinations. If n independently uniform keys choose among m buckets, each fixed pair collides with probability 1/m. There are n(n - 1)/2 pairs, so the expected number of colliding pairs is n(n - 1)/(2m). The pair indicators need not be independent for their expectations to add.

This is the same counting idea behind birthday collisions: the number of possible pairs grows quadratically. For a collision event C, its indicator is no larger than the total number of colliding pairs, so P(C) is at most that expectation. This is useful as an upper bound when n is small relative to the square root of m; an upper bound greater than 1 provides no useful probability estimate.

To bound long runs of heads, consider each possible starting position for k consecutive tosses. Under independent fair tosses, that particular run has probability 2^-k. The probability that any such run occurs is at most the sum over starting positions, no more than n/2^k. This union bound does not require the different run events to be independent.

Try this: with 100 tosses, bound the probability of a run of at least 10 heads by 100/1024. Explain why this bound is not an exact probability.

Practice: [808. Soup Servings](https://leetcode.com/problems/soup-servings/) practices probability states and recurrence. It does not replace the indicator and union-bound derivations above.

## Review

Explain why expected, amortized, and worst-case bounds are different. On a later day, derive the dynamic-array bound from the copy sizes instead of rereading the conclusion.
