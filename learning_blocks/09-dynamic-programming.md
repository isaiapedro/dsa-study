# 9. Dynamic programming

Dynamic programming stores answers to smaller problems so repeated work is avoided. The central step is choosing what one stored answer means.

## 9.1 States, transitions, and base cases

A state contains enough information to describe a smaller problem. A transition builds its answer from already defined states. Base cases stop the recurrence. Finally, choose an order in which all dependencies are available.

Suppose ways[i] counts sequences of steps of length 1 or 2 that reach position i. Every nonempty sequence ends in one of those two steps, so ways[i] = ways[i - 1] + ways[i - 2]. Set ways[0] = 1 for the empty sequence and ways[1] = 1. The first values are 1, 1, 2, 3, 5.

Memoization starts with recursive calls and stores answers as they are requested. Bottom-up evaluation fills them in dependency order. Both can take O(n) here. Keeping only the last two values reduces extra space to O(1), but loses the full table.

Try this: complete ways[5] before reading further. It is 5 + 3 = 8. Explain what would go wrong if ways[0] were zero.

Practice: [70. Climbing Stairs](https://leetcode.com/problems/climbing-stairs/).

## 9.2 Choices over amounts and capacities

For minimum coins, let best[a] be the fewest coins needed for amount a. Set best[0] = 0 and unreachable amounts to infinity. For every allowed coin c ≤ a, consider 1 + best[a - c]. Choose the smallest reachable candidate.

For coins [1, 3, 4] and amount 6, a greedy first choice of 4 leaves two 1s, requiring three coins. Dynamic programming discovers 3 + 3, requiring two. With A amounts and k coin types, the straightforward table takes O(Ak) time and O(A) space.

Rod cutting has the same choice structure with maximization: best[length] chooses a first piece and combines its price with the best value of the remainder. In 0/1 knapsack, each item may be used once, so the state must also respect which items are available. A one-dimensional implementation iterates capacities downward to prevent using the same item repeatedly. Unlimited reuse usually needs the opposite order.

Try this: with one item of weight 2 and value 5, capacity 4 must not produce value 10 in 0/1 knapsack. Trace why increasing capacities would incorrectly allow that.

Practice: [322. Coin Change](https://leetcode.com/problems/coin-change/) and [416. Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/).

## 9.3 Sequences and reconstruction

For longest common subsequence, let dp[i][j] be the best length using the first i characters of one string and the first j of the other. If the last characters agree, use 1 + dp[i - 1][j - 1]. Otherwise use the larger of dp[i - 1][j] and dp[i][j - 1]. Empty prefixes have answer zero.

For "ace" and "abc", the common subsequence "ac" has length 2. A subsequence preserves order but may skip characters; a substring must be contiguous. The table takes O(mn) time. Two rows save memory when only the length is needed.

To recover an actual subsequence, keep the table or explicit choices, then walk backward along the decisions. Equal-length alternatives can produce different valid answers. Edit distance uses a similar prefix table but compares insertion, deletion, and substitution costs.

Try this: explain why matching the last characters lets you shorten both prefixes. Complete the last row for "ab" and "ac".

Practice: [1143. Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/) and [72. Edit Distance](https://leetcode.com/problems/edit-distance/).

## 9.4 Interval dynamic programming

An interval state describes a contiguous range. Try every possible split or final choice inside that range and combine the smaller intervals. Fill short intervals before long ones.

For matrix-chain multiplication, multiplying a p×q matrix by a q×r matrix costs pqr scalar multiplications. Three matrices of sizes 4×2, 2×7, and 7×3 can be grouped two ways. The first grouping costs 4×2×7 + 4×7×3 = 140. The second costs 2×7×3 + 4×2×3 = 66. Both give the same final dimensions, but not the same work.

For a chain i through j, test every split k: left_cost + right_cost + dimensions[i-1] × dimensions[k] × dimensions[j]. There are O(n²) states and O(n) splits each, giving O(n³) time and O(n²) space.

Try this: write the two groupings for dimensions 3, 5, 2, 4 and compare their costs before filling a larger table.

Practice: [1039. Minimum Score Triangulation of Polygon](https://leetcode.com/problems/minimum-score-triangulation-of-polygon/) and [312. Burst Balloons](https://leetcode.com/problems/burst-balloons/). These practice interval splits, not matrix multiplication itself.

## 9.5 Optimal search trees

A balanced search tree minimizes a worst-case height scale. An optimal search tree instead minimizes expected search cost when some keys or unsuccessful search gaps are more likely than others.

Choose a root for a sorted key interval. Every search assigned to either child subtree gains one extra comparison, so add the total probability weight of the interval to the children's best costs. Try each root and keep the least expensive choice.

If key A is requested 90% of the time and B 10%, putting A at the root gives expected successful-search comparisons 0.9×1 + 0.1×2 = 1.1. Reversing them gives 1.9. With unsuccessful searches included, probabilities for gaps also contribute, and empty-subtree base cases carry those gap weights. A direct implementation uses O(n³) time and O(n²) space.

Try this: reverse the two probabilities. Which root should change, and why is alphabetical order alone insufficient to choose it?

Practice: [96. Unique Binary Search Trees](https://leetcode.com/problems/unique-binary-search-trees/) is related root-and-subtree recurrence practice. For the actual optimization, independently compute costs for three keys with chosen probabilities.

## Review

Before coding, say exactly what one table entry means, which entries it reads, and where the answer lives. Later, compare greedy coin choice with the dynamic program using a fresh counterexample.
