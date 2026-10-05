# 14. String sorting, tries, and matching

String algorithms use character order, shared prefixes, or repeated text patterns. Count characters examined, not just the number of strings.

## 14.1 String sorting

Lexicographic order compares the first different character; if one string is a prefix of another, the shorter comes first. Comparing two length-L strings may inspect O(L) characters, so string comparison is not automatically O(1).

Least-significant-digit radix sorting processes fixed-width strings from the final character toward the first, using a stable character sort at every position. Earlier passes order suffixes; stability preserves that work when the next character is considered. With n strings of width W and alphabet size R, time is O(W(n + R)).

Most-significant-digit sorting groups by the first character, then recursively sorts each group by the next. A special end-of-string value must come before ordinary characters. Three-way string quicksort groups strings by character less than, equal to, or greater than a pivot; only the equal group advances its character position.

Try this: sort "ax", "ab", "bx" using stable last-character and then first-character passes. Explain why stability is necessary.

Practice: [14. Longest Common Prefix](https://leetcode.com/problems/longest-common-prefix/) practices shared-prefix comparisons. Separately implement one stable character-sorting pass to practice radix sorting itself.

## 14.2 Tries and ternary search tries

A trie stores one character per path step. Strings sharing a prefix share those nodes. Mark complete words separately from prefixes: after inserting "car" and "cart", the node after r is both a word ending and a parent.

Lookup follows the query's characters. Insertion creates missing edges. Prefix lookup stops after the prefix, then explores descendants. Deleting a word clears its ending marker and removes only nodes no other word needs.

With constant-time child access, searching a length-L key takes O(L). A full R-way child array uses substantial memory; maps trade that space for lookup overhead. A ternary search trie uses left, middle, and right links: compare a character to the node's character, advance in the string only on the middle link, and search left or right otherwise. Its cost also depends on how character-search branches are balanced.

Try this: insert "to", "tea", and "ten". Which node is shared by all three, and which is shared only by the last two?

Practice: [208. Implement Trie (Prefix Tree)](https://leetcode.com/problems/implement-trie-prefix-tree/) and [211. Design Add and Search Words Data Structure](https://leetcode.com/problems/design-add-and-search-words-data-structure/).

## 14.3 Naive matching, rolling hashes, and Boyer–Moore

Exact matching finds occurrences of a pattern of length m in text of length n. Trying the pattern at every possible start takes O(nm) in the worst case, especially on repetitive text.

Rabin–Karp computes a hash of the pattern and a rolling hash for each length-m text window. Remove the outgoing character's contribution, shift the remaining hash, and add the incoming character. Hash equality suggests a candidate, but exact matching must verify characters because collisions are possible. Good hashing can make candidate checks rare; collision-heavy input can still produce O(nm) work.

Boyer–Moore compares from the pattern's right end. A mismatch can justify shifting past alignments ruled out by the mismatching character or by a matched suffix. Large skips can make it effective, but the guarantee depends on which rules and refinements are implemented; a simple bad-character-only variant is not universally linear.

Try this: align pattern "cat" over text "xxcat". Which candidate starts fail immediately? Complete one rolling-window update using your own small alphabet encoding.

Practice: [28. Find the Index of the First Occurrence in a String](https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/).

## 14.4 Finite automata and KMP

A matching automaton keeps the length of the pattern prefix currently matched. Each new character chooses the next state. Reaching state m reports a full match. A full transition table gives constant-time transitions but may need O(mR) preprocessing and space for alphabet size R.

Knuth–Morris–Pratt, or KMP, avoids restarting from scratch after a mismatch. Its prefix table records the longest proper prefix that is also a suffix of each pattern prefix. For "abab", the table is [0, 0, 1, 2].

After matching "abab" and then seeing a mismatch for the next required character, fall back to the shorter matched prefix described by the table. The text position stays in place while the possible prefix length shrinks. Successful extensions increase that length and failures decrease it, which bounds the total fallback work. Building the table and searching take O(m + n) time and O(m) extra space.

Try this: compute the prefix table for "abac": [0, 0, 1, __]. The last value is 0. Explain why the preceding a cannot help with the final c.

Practice: [459. Repeated Substring Pattern](https://leetcode.com/problems/repeated-substring-pattern/) and [28. Find the Index of the First Occurrence in a String](https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/).

## 14.5 Suffix arrays and repeated text

A suffix starts at one text position and continues to the end. A suffix array lists starting positions in lexicographic order of their suffixes. For "aba", suffixes are "aba", "ba", and "a"; sorted starts are [2, 0, 1].

A pattern can be found by binary search over sorted suffixes. A straightforward search compares up to m characters per comparison, giving O(m log n). The longest common prefix, or LCP, of adjacent sorted suffixes helps find repeated substrings: occurrences sharing a prefix appear together.

Constructing and sorting complete suffix strings can cost O(n²) storage or worse comparison work. Prefix doubling instead ranks prefixes of lengths 1, 2, 4, and so on. Sort pairs of previous ranks; after O(log n) rounds all suffixes are ordered. Comparison sorting each round gives O(n log² n); integer-rank sorting can improve it.

Try this: list the four suffixes of "baba" and compute neighboring common-prefix lengths. The longest repeated substring is "ba".

Practice: [1044. Longest Duplicate Substring](https://leetcode.com/problems/longest-duplicate-substring/).

## Review

Choose a trie for shared-prefix dictionary queries, KMP for one exact pattern scan, and a suffix array for a reusable text index. Revisit "abab" later and reconstruct its failure behavior from the meaning of the prefix table.
