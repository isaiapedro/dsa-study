# 2. Arrays, lists, stacks, and queues

An array makes positions easy to find. A linked list makes neighboring nodes easy to reconnect. Stacks and queues describe the order in which items leave a collection; either can be built using arrays or linked nodes.

## 2.1 Arrays, strings, and dynamic arrays

An array gives each item an integer position. In [4, 9, 2], position 0 contains 4 and position 2 contains 2. Valid positions run from 0 through n - 1. A loop may finish at n, but it must not read that position.

A contiguous array computes an item's address from the starting address and the item's width. A Python list stores references in a resizable array, so direct indexing is constant time. Inserting at the front shifts the existing references and takes O(n). Appending is amortized O(1): usually cheap, occasionally expensive when storage grows.

A string is a sequence of characters. Python strings are immutable: changing a character creates new text. Repeatedly building larger strings can copy substantial data; collecting pieces and joining once avoids repeated prefix copying. A displayed character can contain more than one Unicode code point, so indexing text does not always select one visible symbol.

Try this: insert 7 at index 1 in [4, 9, 2]. Move 2 right, then 9, then write 7. Complete the moves for deleting index 0.

Practice: [1929. Concatenation of Array](https://leetcode.com/problems/concatenation-of-array/) and [344. Reverse String](https://leetcode.com/problems/reverse-string/). The latter provides a mutable character array.

## 2.2 Linked lists

A linked-list node stores a value and a reference to the next node. The head identifies the first node. The final node points to nothing. Finding position k requires walking through earlier nodes, so it takes O(k).

For A → B → C, inserting X after A sets X.next to B and then A.next to X. Reversing these assignments without saving B can lose access to the remaining list. Removing B after a known A sets A.next to C. Those local changes take O(1); locating A may take O(n).

To reverse a list, keep three references: the reversed prefix, the current node, and the saved next node. Save the next node before turning the current link backward. Each step lengthens the reversed prefix and shortens the untouched suffix.

Try this: after reversing A in A → B → C, the reversed prefix is A → nothing and the current node is B. Complete B's step. A dummy head simplifies edits that might replace the real head.

Practice: [206. Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) and [21. Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/).

## 2.3 Stacks, queues, and deques

A stack removes the most recently added item first. Push A, then B; pop returns B. This matches unfinished recursive calls, undo operations, and nested parentheses. A queue removes the oldest item first. Enqueue A, then B; dequeue returns A. This matches work arriving in order.

A deque supports both ends. In Python, collections.deque supports efficient additions and removals at either end. Removing index 0 from a list shifts all remaining items, so it is a poor queue operation.

To check brackets, push opening brackets. Each closing bracket must match the top opening bracket. For "([])", the stack changes from empty to "(" to "([" to "(" to empty. Reject a closing bracket when the stack is empty, and reject leftover openings at the end.

Try this: finish the trace for "([)]". The first closing parenthesis disagrees with the top "[", so the string is invalid even though counts match.

Practice: [20. Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) and [232. Implement Queue using Stacks](https://leetcode.com/problems/implement-queue-using-stacks/).

## 2.4 Trees as linked structures

A binary-tree node has up to two children, called left and right. A general tree can have any number of children. An array of child lists represents a general tree directly; a first-child/next-sibling representation uses two links per node instead.

A traversal visits the nodes in a chosen order. Preorder visits a node before its children. Postorder visits children before their parent. Inorder visits left subtree, node, then right subtree and is specific to binary trees.

Suppose a root 6 has left child 2 and right child 9. Preorder is 6, 2, 9; inorder is 2, 6, 9; postorder is 2, 9, 6. Inorder is sorted only when the tree also satisfies the binary-search-tree ordering rule.

Try this: attach 4 as the right child of 2 and complete each order. Traversal takes O(n), while a recursive implementation uses O(h) call-stack space for height h.

Practice: [144. Binary Tree Preorder Traversal](https://leetcode.com/problems/binary-tree-preorder-traversal/) and [590. N-ary Tree Postorder Traversal](https://leetcode.com/problems/n-ary-tree-postorder-traversal/).

## Review

Explain which costs include finding a node and which assume the node is already known. Before practice, name the input and answer, the relevant limit, the information kept between steps, and why the chosen structure fits. Later, reverse a fresh three-node list without looking at the example.
