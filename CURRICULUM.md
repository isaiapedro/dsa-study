# Curated CS Curriculum

This is project-authored study guidance. It is deliberately separate from the
LeetCode catalog in `data/` and its generated `site/`: this file contains no
problem statements, scraped examples, account data, or solution history.

The links below are pointers to public learning resources. Read them in a
browser when useful; do not download their content into this project unless a
future decision explicitly establishes a licensing and storage policy.

## How to use this guide

Work through a concept in order: state its invariant or contract, implement a
small version from memory, analyse its time and space cost, then use the local
catalog to find problems carrying the matching official topic tag. A solved
problem is practice evidence, not a replacement for understanding the model.

## Foundations

### Cost models and correctness

**Note.** Describe work as a function of input size, name the dominant
operation, and account for auxiliary memory separately from the input. For a
loop invariant, write what is true before each iteration, show that one step
preserves it, and show that termination establishes the desired result.

**Read.** [MIT 6.006: Introduction to Algorithms](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/) for an algorithms course with readings, notes, and exercises; [Algorithms, 4th Edition](https://algs4.cs.princeton.edu/home/) for analysis and implementation-oriented reference material.

### Arrays, strings, and linked structures

**Note.** Arrays trade fixed indexing for costly middle insertion; linked
structures trade traversal time for local rewiring. Two pointers require a
clear monotonicity argument. Sliding windows work when expanding and shrinking
the window preserves a useful condition.

**Practice lens.** State what each pointer bounds and whether every pointer
only moves forward. This turns an apparent nested loop into a linear amortized
argument when appropriate.

## Core data structures

### Stacks, queues, and hashing

**Note.** A stack models last-in, first-out state; a queue models first-in,
first-out work. Hash tables offer expected constant-time lookup only under a
specified collision strategy and load factor; do not claim a worst-case bound
without qualifying it.

**Read.** [Princeton’s fundamentals and searching chapters](https://algs4.cs.princeton.edu/home/) cover stacks, queues, symbol tables, and hash tables.

### Trees, heaps, and disjoint sets

**Note.** Tree algorithms should identify the traversal order and the value
returned by each subtree. A binary heap maintains an ordering relation only
between a node and its children, not a globally sorted layout. Union-find
combines components efficiently when path compression and union by rank/size
are used together.

**Read.** [cp-algorithms: data structures](https://cp-algorithms.com/data_structures/) is a focused reference for disjoint sets and range-query structures; use its material as a reference rather than importing it.

## Algorithmic techniques

### Sorting, searching, and divide and conquer

**Note.** Binary search needs an explicit monotone predicate and interval
convention. Divide and conquer needs a recurrence that includes both subproblem
cost and combine cost. Stable sorting preserves the relative order of equal
keys; in-place sorting describes auxiliary-space use, not necessarily input
mutation safety in every language API.

**Read.** [Princeton’s sorting chapter](https://algs4.cs.princeton.edu/20sorting/) and [MIT 6.006 course materials](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/).

### Graphs

**Note.** Choose the representation before the traversal: adjacency lists are
usually appropriate for sparse graphs, while matrices make edge tests direct.
BFS finds shortest paths by edge count in an unweighted graph; Dijkstra’s
algorithm requires non-negative edge weights. A topological order exists
exactly for directed acyclic graphs.

**Read.** [Princeton’s graph chapter](https://algs4.cs.princeton.edu/40graphs/) for traversal, shortest paths, and minimum spanning trees.

### Dynamic programming and greedy choice

**Note.** A dynamic-programming state must contain enough information to make
the remaining subproblem independent of earlier choices. Define the state,
transition, base cases, evaluation order, and answer location before coding.
A greedy algorithm needs an exchange argument or another proof that a locally
optimal choice can occur in some global optimum.

**Read.** [cp-algorithms: dynamic programming](https://cp-algorithms.com/dynamic_programming/intro-to-dp.html) for a compact implementation reference, and the [MIT course](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/) for broader algorithmic analysis.

## Advanced practice topics

### Backtracking, bit manipulation, and strings

**Note.** Backtracking explores a decision tree; pruning must be justified by a
constraint that cannot be repaired below the current state. Bit operations are
integer operations, so write down the bit-width and signedness assumptions.
For string matching, distinguish preprocessing cost from per-query cost.

**Read.** [cp-algorithms](https://cp-algorithms.com/) indexes bit manipulation, string algorithms, and combinatorics in one maintained reference.

## Boundaries and maintenance

- Keep factual, personal progress notes out of this file; future private
  tracking belongs in an ignored local store.
- Keep imported LeetCode material in the ignored `data/` and `site/` paths.
- Add a source only after checking its access terms and relevance. Store a link
  and a short purpose statement here; do not copy source text.
- Review links periodically. A broken or changed resource should be replaced
  with another link, not mirrored locally by default.
