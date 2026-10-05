# 3. Searching arrays and using windows

Searching becomes faster when a property lets you safely ignore candidates. Sorted order supports binary search and opposing pointers. A useful condition on a contiguous interval can support a sliding window.

## 3.1 Linear and binary search

Linear search checks values until it finds a match or reaches the end. It works without sorted order and takes O(n) in the worst case. Binary search requires sorted order or an equivalent yes/no property that changes only once.

Use an interval [left, right): left is included and right is excluded. Start at [0, n). To find the first value at least target, inspect mid = (left + right) // 2. If a[mid] is too small, set left = mid + 1. Otherwise set right = mid. Any possible first qualifying value remains in the interval or at its final boundary.

For [2, 5, 5, 8] and target 5, start [0, 4). Midpoint 2 qualifies, giving [0, 2). Midpoint 1 qualifies, giving [0, 1). Midpoint 0 fails, giving [1, 1). Return 1. Returning n means no value qualifies.

Try this: repeat for target 9. Why must the final index be checked before reading the array? Binary search uses O(log n) comparisons and O(1) extra space.

Practice: [704. Binary Search](https://leetcode.com/problems/binary-search/) and [35. Search Insert Position](https://leetcode.com/problems/search-insert-position/).

## 3.2 Two pointers

On a sorted array, one pointer at each end can search for a target pair sum. If the sum is too small, move the left pointer right. Every pair using that old left value and a smaller right value is also too small. If the sum is too large, move the right pointer left for the symmetric reason.

For [1, 4, 6, 10] and target 10, 1 + 10 is too large, so discard 10. Now 1 + 6 is too small, so discard 1. The next pair, 4 + 6, succeeds. Each pointer moves at most n positions, so the scan takes O(n).

Sorting an unsorted input first costs O(n log n) and may destroy the original position order. A hash table is often a better choice when the answer needs original indices. Two pointers also serve other tasks, such as compacting an array with read and write positions; the justification then concerns which items have been retained.

Try this: use [2, 3, 7, 12] with target 9. Explain the discarded pairs at each move.

Practice: [167. Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) and [26. Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/).

## 3.3 Sliding windows

A window is a contiguous part of an array or string. Extend its right end to include new items; move its left end to restore the desired condition. The key question is whether a discarded left position can ever become useful again.

For the longest substring without repeated characters, keep counts inside the window. On reading "abca", the last a causes a duplicate. Remove characters from the left until the first a is gone. The remaining window "bca" is valid. Each character enters and leaves at most once, giving O(n) expected time with a hash table.

For positive numbers, a window sum grows when the right end moves and shrinks when the left end moves. This supports finding the shortest interval with sum at least a target. Negative values break that argument: removing a negative number increases the sum.

Try this: trace target 7 over [2, 4, 3]. The full window totals 9; dropping 2 leaves 7 and a shorter answer. Complete the next attempted drop and explain why it stops.

Practice: [3. Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) and [209. Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/).

## 3.4 Prefix sums and searching an answer

A prefix sum stores totals before each position: prefix[0] = 0 and prefix[i + 1] = prefix[i] + a[i]. The sum of a[left:right] is prefix[right] - prefix[left]. For [3, -2, 5], prefixes are [0, 3, 1, 6]; the last two values sum to 6 - 3 = 3.

Prefix sums take O(n) preprocessing and O(1) per range-sum query. Unlike the positive-number sliding-window argument, subtraction works with negative values. To count subarrays with sum k, count earlier prefix totals equal to current_total - k. Record the empty prefix once.

Binary search can also search possible answers. If a processing speed is sufficient, every faster speed is sufficient. Test the middle speed and keep the half that can contain the first sufficient value. Total time is the number of tests times the cost of one feasibility test; it is not merely O(log n).

Try this: complete the prefixes for [2, -1, 4], then find the sum over indices 1 through 2.

Practice: [560. Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) and [875. Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/).

## Review

Without notes, give one reason binary search works, one reason two pointers work, and one input property that breaks a positive-sum window. Revisit with duplicates, an empty array, and negative numbers.
