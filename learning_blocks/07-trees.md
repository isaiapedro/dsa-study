# 7. Search trees and larger indexes

A search tree stores keys in an order that helps choose the next branch. A balanced tree keeps paths short. An augmented tree stores extra summaries, and a B-tree groups many keys into each node to reduce storage accesses.

## 7.1 Binary search trees

In a binary search tree with distinct keys, every key in the left subtree is smaller than the node's key, and every key in the right subtree is larger. Decide how duplicates are represented, for example by a count at one node.

To find 7 in a tree rooted at 5, go right; if the next node is 9, go left. Each comparison discards an entire subtree. Search, insertion, and deletion take O(h), where h is the tree height. Inserting sorted keys without balancing can produce a chain with h = Θ(n).

Delete a leaf by removing its link. Delete a node with one child by linking its parent directly to the child. For two children, replace the key with its inorder successor, the smallest key in its right subtree, then remove that successor from its old position. The successor has no left child, making the second deletion simpler.

Try this: insert 5, 2, 9, 7, then delete 5. Explain why 7 is a valid replacement. Inorder traversal lists the keys in sorted order.

Practice: [700. Search in a Binary Search Tree](https://leetcode.com/problems/search-in-a-binary-search-tree/) and [450. Delete Node in a BST](https://leetcode.com/problems/delete-node-in-a-bst/).

## 7.2 Balanced trees and rotations

A rotation changes a few links while preserving inorder order. In a right rotation, a node's left child moves up, and that child's right subtree becomes the old root's left subtree. Every moved subtree remains between the same surrounding key values.

A red-black tree uses colors to control height: the root and absent leaves are black, a red node has no red child, and every path from a node to an absent leaf has the same number of black nodes. These rules keep height O(log n), at most twice the logarithmic black-height scale.

Insertion starts like ordinary search-tree insertion, often with a red new node. A red parent creates a conflict. A red uncle allows recoloring upward; a black uncle requires rotations and recoloring, first straightening a bent parent-child shape if necessary. Deleting a black node can remove one black contribution from a path. Repair examines the sibling: expose a black sibling if needed, propagate a shortage when both sibling children are black, or rotate toward a red child and redistribute colors to restore equal black counts.

A 2–3 tree expresses balancing with nodes holding one or two keys and equal leaf depth. Red-black links can encode such multi-key nodes.

Try this: rotate a tree with root 8, left child 4, and 4's right child 6. The sorted order remains 4, 6, 8.

Practice: [1382. Balance a Binary Search Tree](https://leetcode.com/problems/balance-a-binary-search-tree/). This practices balancing by rebuilding, not red-black insertion or deletion; trace the color repairs separately on paper.

## 7.3 Subtree sizes and interval trees

Augmentation adds information that can be updated from a node and its children. Store size = 1 + left_size + right_size. If the left subtree has three nodes, the current node has rank four within its subtree. To find rank k, go left when k ≤ 3, return the current node when k = 4, and otherwise search right for rank k - 4.

Update summaries after insertions, deletions, and rotations. Because only a constant number of nodes change directly in a rotation, summaries built from child values can often be repaired locally. A balanced tree then supports rank and selection in O(log n).

An interval tree orders intervals by their lower endpoints and stores the largest upper endpoint in each subtree. For closed intervals, [a, b] overlaps [c, d] exactly when a ≤ d and c ≤ b. If a left subtree's maximum endpoint is less than c, none of its intervals can overlap [c, d], so that branch can be skipped.

Try this: can a subtree whose maximum endpoint is 6 contain an interval overlapping [8, 10]? No. Complete a rank search using left sizes 3, then 1.

Practice: [230. Kth Smallest Element in a BST](https://leetcode.com/problems/kth-smallest-element-in-a-bst/) and [729. My Calendar I](https://leetcode.com/problems/my-calendar-i/). The calendar is an interval application, not a requirement to implement this exact tree.

## 7.4 B-trees and storage blocks

A B-tree stores several sorted keys per node. A node with k keys can have k + 1 children, separating the key ranges. All leaves lie at the same depth. For minimum degree t, nonroot nodes hold between t - 1 and 2t - 1 keys; the root has special minimum-size rules.

Search within one node, then descend into the matching range. A node can fit a storage page, so high branching reduces the number of page reads to O(log_t n). This is an I/O bound; comparisons within a page still cost work.

When a node is full, split it and move its middle key into the parent. During deletion, borrow from a sufficiently full sibling through the parent or merge siblings with a separating parent key. Maintaining enough keys before descending prevents an underfull child from being left unresolved. A root with no keys can be replaced by its only child.

Try this: with t = 2, split [3, 6, 9]. Promote 6 and leave [3] and [9] as children.

Practice: [98. Validate Binary Search Tree](https://leetcode.com/problems/validate-binary-search-tree/) is related range-validation practice. LeetCode does not replace a B-tree exercise: independently implement search and a root split in a small multi-key tree.

## Review

Distinguish a search tree's order, a balanced tree's height, an augmented tree's summaries, and a B-tree's page layout. Reconstruct a rotation later without using the example.
