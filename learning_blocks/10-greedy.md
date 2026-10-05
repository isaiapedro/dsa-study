# 10. Greedy choices and online decisions

A greedy algorithm commits to a locally attractive choice. It is correct only when that choice can be part of an optimal overall answer. An online algorithm makes decisions before future input is known.

## 10.1 Choosing compatible intervals

To select as many nonoverlapping intervals as possible, repeatedly choose the available interval with earliest finish time. Sort by finish time, then accept an interval when its start is at least the last selected finish, assuming touching endpoints are allowed.

Why does this work? Take an optimal schedule and replace its first interval with the earliest-finishing interval. The replacement ends no later, so it leaves at least as much room for the remaining schedule. Repeat the argument on what remains. This replacement argument is called an exchange argument.

For [1, 3), [2, 5), [3, 4), choose [1, 3) then [3, 4). Choosing the longest interval first would leave fewer choices. Sorting takes O(n log n); the scan takes O(n). Weighted intervals change the problem: the greatest count need not give the greatest reward, so a dynamic program may be needed.

Try this: add [4, 7) and complete the selected schedule. Then invent rewards that make the count-maximizing answer less valuable.

Practice: [435. Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/).

## 10.2 Huffman coding and greedy proof

A prefix-free binary code gives each symbol a bit string such that no symbol's code begins another symbol's code. A binary tree represents it: left and right edges are bits, and symbols appear only at leaves. Frequent symbols should have shorter paths.

Huffman's algorithm repeatedly merges the two least frequent remaining trees. Put their combined frequency back in a min-heap. For frequencies 2, 3, and 7, merge 2 and 3 into 5, then merge 5 and 7 into 12. The rare symbols have length 2 and the common one length 1, for weighted length 2×2 + 3×2 + 7×1 = 17.

An optimal tree can place two least-frequent symbols as deepest siblings: exchanging them with deeper, more frequent leaves cannot increase cost. Contract those siblings into one combined symbol and solve the smaller problem. That connects the greedy choice to an optimal solution. For k symbols, heap construction and merges take O(k log k).

Try this: complete the merges for 1, 4, 5, 9. Keep the tree, since the merge total alone does not encode messages.

Practice: [1167. Minimum Cost to Connect Sticks](https://leetcode.com/problems/minimum-cost-to-connect-sticks/) is a related optimal-merge exercise; access may require a subscription. The original frequency example above supplies local practice without it.

## 10.3 Offline and online caching

A cache holds a limited number of items. A hit finds an item already present; a miss requires loading it. When full, an eviction policy chooses what to remove.

If the entire future request sequence is known, evict the item whose next use is farthest away, or never occurs again. This offline rule is optimal for minimizing misses under equal item sizes and equal miss costs. An exchange argument compares it with an optimal schedule that evicts something used sooner; swapping the choices cannot force an earlier extra miss.

An online cache cannot see future requests. Least recently used, or LRU, evicts the item whose last use is oldest. A dictionary plus a doubly linked list supports lookup, movement, and eviction in expected O(1). LRU is useful but does not match the offline optimum on every sequence.

Try this: with capacity 2 and requests A, B, A, C, B, trace LRU. At C, it evicts B; the next request misses. The offline rule would evict A.

Practice: [146. LRU Cache](https://leetcode.com/problems/lru-cache/).

## 10.4 Competitive analysis and online trade-offs

Competitive analysis compares an online algorithm's cost with an optimal algorithm that knows the future, on the same request sequence. An r-competitive algorithm costs at most r times the optimum, possibly plus a fixed additive constant.

Suppose renting costs 1 per day and buying costs B. Rent until the accumulated rental cost reaches B, then buy if another day is needed. If use ends early, you have paid only for the days used. If it lasts, total spending is at most about 2B, while the offline optimum pays B. This gives a factor-2 bound under that cost model.

Waiting before dispatching an elevator has a similar uncertainty: serving immediately reduces current delay but may miss an opportunity to combine nearby requests. Any guarantee must specify whether cost means movement, waiting, or something else. A self-organizing search list has another online choice: moving each accessed item to the front favors recently requested items. Its classic competitive guarantee assumes the list-update cost model, including allowed free forward moves.

Try this: take B = 6 and compare use lasting 3 days with use lasting 20 days. Explain why the correct hindsight choice differs.

Practice: [1409. Queries on a Permutation With Key](https://leetcode.com/problems/queries-on-a-permutation-with-key/) directly exercises move-to-front behavior. It does not establish a competitive ratio.

## Review

Give a counterexample to a tempting greedy rule, then explain why earliest finish avoids that failure for unweighted intervals. Revisit the cache sequence later and distinguish information available online from hindsight.
