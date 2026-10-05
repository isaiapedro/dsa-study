"""Exact textbook-page links for every authored lesson section.

The URLs point to lawful Google Books records for the two governed editions. They
are navigation links only: a preview can be limited by the rights holder and no
book content is copied or downloaded by DSA Study.
"""

from __future__ import annotations

from collections.abc import Iterable

CLRS = "RSMuEAAAQBAJ"
SEDGEWICK_WAYNE = "GhsNBQAAQBAJ"


def _clrs(page: int, detail: str) -> tuple[str, str]:
    return (f"CLRS, 4th ed., p. {page} ({detail})", f"https://books.google.com/books?id={CLRS}&pg=PA{page}")


def _sw(page: int, detail: str) -> tuple[str, str]:
    return (f"Sedgewick/Wayne, 4th ed., p. {page} ({detail})", f"https://books.google.com/books?id={SEDGEWICK_WAYNE}&pg=PA{page}")


# The page is the opening page of the named section or of the closest stated
# textbook treatment. Each lesson is original: this map is a reading guide, not
# a claim that a short lesson replaces every proof or exercise on that page.
SECTION_PAGES: dict[str, dict[str, tuple[tuple[str, str], ...]]] = {
    "01-foundations": {
        "1.1": (_clrs(17, "Getting Started"), _sw(17, "Basic Programming Model")),
        "1.2": (_clrs(49, "Characterizing Running Times"),),
        "1.3": (_clrs(1140, "Summations"), _clrs(1178, "Counting and Probability")),
        "1.4": (_clrs(1153, "Sets, relations, functions, graphs, and trees"),),
        "1.5": (_clrs(1178, "Counting and Probability"), _clrs(1214, "Matrices")),
        "1.6": (_clrs(5, "The Role of Algorithms in Computing"), _sw(17, "Basic Programming Model")),
    },
    "02-arrays": {
        "2.1": (_clrs(252, "Array-based data structures"), _sw(121, "Bags, Queues, and Stacks")),
        "2.2": (_clrs(258, "Linked lists"), _sw(143, "Linked-list representation")),
        "2.3": (_clrs(252, "Stacks and queues"), _sw(121, "Bags, Queues, and Stacks")),
        "2.4": (_clrs(265, "Representing rooted trees"),),
    },
    "03-searching": {
        "3.1": (_sw(47, "Binary search"),),
        "3.2": (_sw(17, "Basic Programming Model"),),
        "3.3": (_sw(363, "Symbol Tables"),),
        "3.4": (_sw(363, "Symbol Tables"),),
    },
    "04-sorting": {
        "4.1": (_sw(245, "Elementary Sorts"),),
        "4.2": (_clrs(17, "Insertion sort and merge-sort introduction"), _sw(273, "Mergesort")),
        "4.3": (_clrs(182, "Quicksort"), _sw(289, "Quicksort")),
        "4.4": (_clrs(161, "Heaps and priority queues"),),
        "4.5": (_clrs(205, "Sorting in Linear Time"),),
        "4.6": (_clrs(227, "Medians and Order Statistics"),),
    },
    "05-analysis": {
        "5.1": (_clrs(76, "Divide-and-Conquer"),),
        "5.2": (_clrs(90, "Substitution method for recurrences"), _clrs(95, "Recursion-tree method")),
        "5.3": (_clrs(126, "Probabilistic Analysis and Randomized Algorithms"),),
        "5.4": (_clrs(448, "Amortized Analysis"),),
        "5.5": (_clrs(130, "Indicator random variables"),),
    },
    "06-hashing": {
        "6.1": (_clrs(272, "Hash Tables"), _sw(459, "Hash Tables")),
        "6.2": (_clrs(275, "Hash tables and collision resolution"), _sw(459, "Hash Tables")),
        "6.3": (_clrs(282, "Hash functions"), _sw(459, "Hash Tables")),
        "6.4": (_sw(363, "Symbol Tables"),),
    },
    "07-trees": {
        "7.1": (_clrs(312, "Binary Search Trees"), _sw(396, "Binary Search Trees")),
        "7.2": (_clrs(331, "Red-Black Trees"), _sw(425, "Balanced Search Trees")),
        "7.3": (_clrs(480, "Dynamic order statistics"),),
        "7.4": (_clrs(497, "B-Trees"),),
    },
    "08-union-find": {
        "8.1": (_clrs(520, "Data Structures for Disjoint Sets"),),
        "8.2": (_clrs(527, "Disjoint-set forests"),),
        "8.3": (_clrs(520, "Data Structures for Disjoint Sets"),),
        "8.4": (_clrs(520, "Data Structures for Disjoint Sets"),),
    },
    "09-dynamic-programming": {
        "9.1": (_clrs(362, "Dynamic Programming"),),
        "9.2": (_clrs(363, "Rod cutting"),),
        "9.3": (_clrs(393, "Longest common subsequence"),),
        "9.4": (_clrs(373, "Matrix-chain multiplication"),),
        "9.5": (_clrs(400, "Optimal binary search trees"),),
    },
    "10-greedy": {
        "10.1": (_clrs(417, "Greedy Algorithms"),),
        "10.2": (_clrs(431, "Huffman codes"),),
        "10.3": (_clrs(440, "Offline caching"),),
        "10.4": (_clrs(791, "Online Algorithms"),),
    },
    "11-graphs": {
        "11.1": (_clrs(549, "Graph representations"), _sw(519, "Undirected Graphs")),
        "11.2": (_clrs(554, "Breadth-first search"),),
        "11.3": (_clrs(563, "Depth-first search"), _sw(567, "Directed Graphs")),
        "11.4": (_clrs(573, "Topological sort"),),
        "11.5": (_clrs(576, "Strongly connected components"),),
    },
    "12-weighted-graphs": {
        "12.1": (_clrs(585, "Minimum Spanning Trees"), _sw(605, "Minimum Spanning Trees")),
        "12.2": (_clrs(604, "Single-Source Shortest Paths"), _sw(639, "Shortest Paths")),
        "12.3": (_clrs(612, "Bellman-Ford"), _clrs(616, "Shortest paths in DAGs")),
        "12.4": (_clrs(646, "All-Pairs Shortest Paths"),),
        "12.5": (_clrs(662, "Johnson's algorithm"),),
    },
    "13-flow": {
        "13.1": (_clrs(670, "Maximum Flow"),),
        "13.2": (_clrs(676, "Ford-Fulkerson method"),),
        "13.3": (_clrs(693, "Maximum bipartite matching"),),
        "13.4": (_clrs(716, "Stable-marriage problem"),),
        "13.5": (_clrs(723, "Hungarian algorithm"),),
    },
    "14-strings": {
        "14.1": (_sw(703, "String Sorts"),),
        "14.2": (_sw(731, "Tries"),),
        "14.3": (_clrs(960, "Naive string matching"), _clrs(962, "Rabin-Karp")),
        "14.4": (_clrs(967, "Finite automata"), _clrs(975, "Knuth-Morris-Pratt")),
        "14.5": (_clrs(985, "Suffix arrays"),),
    },
    "15-compression": {
        "15.1": (_sw(788, "Regular Expressions"),),
        "15.2": (_sw(810, "Data Compression"),),
        "15.3": (_clrs(431, "Huffman codes"), _sw(810, "Data Compression")),
        "15.4": (_sw(810, "Data Compression"),),
    },
    "16-numerical": {
        "16.1": (_clrs(80, "Matrix multiplication"), _clrs(85, "Strassen's algorithm")),
        "16.2": (_clrs(819, "Solving systems of linear equations"),),
        "16.3": (_clrs(850, "Linear Programming"),),
        "16.4": (_clrs(877, "Polynomials and the FFT"),),
        "16.5": (_clrs(1214, "Matrices and matrix operations"),),
    },
    "17-number-theory": {
        "17.1": (_clrs(903, "Number-Theoretic Algorithms"), _clrs(911, "Greatest common divisor")),
        "17.2": (_clrs(916, "Modular arithmetic"), _clrs(928, "Chinese remainder theorem")),
        "17.3": (_clrs(932, "Powers of an element"), _clrs(942, "Primality testing")),
        "17.4": (_clrs(936, "RSA public-key cryptosystem"),),
        "17.5": (_clrs(903, "Number-Theoretic Algorithms"),),
    },
    "18-parallel": {
        "18.1": (_clrs(748, "Parallel Algorithms"),),
        "18.2": (_clrs(770, "Parallel matrix multiplication"),),
        "18.3": (_clrs(775, "Parallel merge sort"),),
        "18.4": (_sw(856, "Event-Driven Simulation"),),
    },
    "19-learning": {
        "19.1": (_clrs(1003, "Machine-Learning Algorithms"), _clrs(1005, "Clustering")),
        "19.2": (_clrs(1015, "Multiplicative-weights algorithms"),),
        "19.3": (_clrs(1022, "Gradient descent"),),
    },
    "20-hard-problems": {
        "20.1": (_clrs(1042, "NP-Completeness"), _clrs(1061, "NP-completeness and reducibility")),
        "20.2": (_clrs(1080, "NP-complete problems"),),
        "20.3": (_clrs(1104, "Approximation Algorithms"), _clrs(1106, "Vertex cover")),
        "20.4": (_clrs(1115, "Set covering"), _clrs(1119, "Randomization and linear programming")),
        "20.5": (_clrs(1124, "Subset-sum problem"),),
    },
}


def references_for(module_id: str, section: str) -> Iterable[tuple[str, str]]:
    """Return explicit page links for one authored lesson heading."""
    return SECTION_PAGES.get(module_id, {}).get(section, ())
