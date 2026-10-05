# 4. Sorting and selecting

Sorting places values in order. Selection finds a particular rank, such as the fifth smallest value, without necessarily sorting everything. Equal keys introduce another question: does the algorithm preserve their previous order? If so, the sort is stable.

## 4.1 Insertion, selection, and Shell sort

Insertion sort grows a sorted prefix. In [6, 2, 5], insert 2 before 6 to get [2, 6, 5], then insert 5 between them. Before every insertion, the earlier part is sorted; shifting larger values preserves their order and opens the right position. Worst-case time is O(n²), but already sorted input takes O(n). With a strict greater-than comparison when shifting, equal keys stay in order.

Selection sort repeatedly finds the smallest remaining value and swaps it into place. It always makes Θ(n²) comparisons and only O(n) swaps. Ordinary swapping can disturb equal keys, so it is not generally stable.

Shell sort first insertion-sorts positions separated by a gap, then reduces the gap until it reaches 1. A gap of 3 compares positions 0, 3, 6 separately from 1, 4, 7. Early passes move values long distances. Its running-time bound depends on the gap sequence; it has no single universal O(n log n) guarantee.

Try this: perform one insertion and one selection step on [5, 1, 4, 2]. Explain what is guaranteed afterward.

Practice: [912. Sort an Array](https://leetcode.com/problems/sort-an-array/). Use the quadratic sorts on small local cases; use a faster algorithm for the full constraints.

## 4.2 Mergesort

Mergesort divides an array into halves, sorts each half, then merges them. During merging, compare the next unused item in each sorted half and take the smaller. That item is the smallest among all remaining items.

Merge [2, 7] and [3, 5]: take 2, then 3, then 5, then the remaining 7. Each item is copied once at that level. There are O(log n) levels, so array mergesort takes O(n log n) time and typically O(n) extra array space.

When keys tie, take from the left half first to preserve stability. Bottom-up mergesort avoids recursion: merge runs of length 1, then 2, then 4, continuing until one run remains. Linked-list mergesort can relink existing nodes, though recursive calls still need stack space.

Try this: complete a merge of [1, 4, 4] and [2, 4, 8], labeling which half each 4 came from.

Practice: [148. Sort List](https://leetcode.com/problems/sort-list/) and [88. Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/).

## 4.3 Quicksort and partitioning

Quicksort chooses a pivot, groups smaller and larger values around it, and recursively sorts the groups. Partitioning handles one array segment in linear time. Balanced partitions give O(n log n) total time; repeatedly separating one item from the rest gives O(n²).

For [8, 3, 6, 2, 5] with pivot 5, one valid grouping is [3, 2], [5], [8, 6]. The groups are not yet sorted. A three-way partition keeps values less than, equal to, and greater than the pivot separate, avoiding repeated work on many equal keys.

Choosing a pivot randomly makes expected time O(n log n) for every fixed input under independent random choices. It does not eliminate the quadratic worst case. In-place partitioning avoids a second array, but recursion still uses memory; processing the smaller side recursively and the larger side in a loop bounds stack depth.

Try this: partition [4, 4, 1, 7, 4] into three groups. Which group needs no further sorting?

Practice: [75. Sort Colors](https://leetcode.com/problems/sort-colors/) and [912. Sort an Array](https://leetcode.com/problems/sort-an-array/).

## 4.4 Heaps and priority queues

A min-heap keeps every parent no larger than its children. The root is smallest, but siblings and unrelated branches need not be sorted. In an array, index i has children 2i + 1 and 2i + 2.

To insert 3 into a heap holding [2, 6, 4], append it at the end, then swap upward past 6. To remove 2, move the last item to the root and swap it downward with the smaller child until the rule holds. Each path has O(log n) length. Building a heap bottom-up takes O(n), because most nodes are near the bottom and move only a short distance.

Heapsort builds a max-heap, repeatedly swaps the largest value to the end, and repairs the remaining heap. It takes O(n log n), uses O(1) extra array space with iterative repair, and is not stable.

Try this: trace inserting 1 into [2, 3, 4, 6]. Then explain why a heap cannot answer an arbitrary membership query in O(log n).

Practice: [703. Kth Largest Element in a Stream](https://leetcode.com/problems/kth-largest-element-in-a-stream/) and [23. Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/).

## 4.5 Counting, radix, and bucket sorting

Comparison sorting must distinguish n! possible orders of distinct values. A yes/no comparison has two outcomes, so a decision tree needs height at least log₂(n!) = Ω(n log n) in the worst case. Faster sorting must use more information than comparisons alone.

Counting sort counts occurrences of integer keys in a range of size k. Prefix counts give output positions. It takes O(n + k); a stable placement pass supports radix sort. Radix sort processes digits with a stable sort, commonly from the least significant digit upward. With d digits and radix r, this version takes O(d(n + r)).

Bucket sort divides a numeric range into intervals and sorts each interval separately. Expected linear time for a standard bucket construction depends on values being suitably distributed; a crowded bucket can require quadratic work.

Try this: counting-sort [2, 0, 2, 1]. Then explain why using one bucket for every possible 64-bit value is impractical.

Practice: [164. Maximum Gap](https://leetcode.com/problems/maximum-gap/). Compare the information used by radix or bucket methods with comparison sorting.

## 4.6 Ranks, selection, and applications

The kth smallest item is an order statistic. Quickselect partitions around a pivot, then visits only the side containing the desired rank. A random pivot gives expected O(n) time but O(n²) worst-case time. A heap of size k gives O(n log k) time and is convenient for streams.

A deterministic linear-time selection method groups values in fives, finds each group's median, and recursively selects a median of those medians as pivot. Enough values are forced to each side that the recurrence is bounded by T(n/5) + T(7n/10 + O(1)) + O(n), which is O(n).

Sorting also makes duplicates adjacent, allows two sorted collections to be merged, and orders events or intervals before scanning. Define a consistent comparison; a rule that says A precedes B, B precedes C, and C precedes A cannot define a sorted order.

Try this: after partitioning around the fifth-smallest item, which side can contain the third smallest? Only the left side.

Practice: [215. Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) and [56. Merge Intervals](https://leetcode.com/problems/merge-intervals/).

## Review

Choose a sort for nearly sorted data, a guaranteed time bound with small extra space, and stable ordering. Explain your choices before implementing one on a fresh example.
