# 6. Hash tables and symbol tables

A symbol table associates each key with a value. A phone directory maps a name to a number; a frequency table maps a word to its count. A set needs only the keys.

## 6.1 Direct addressing and key-value lookup

If keys are small integers from 0 to U - 1, use a U-entry array and store each key at its own position. Lookup is O(1), but space is Θ(U), even when only a few keys are present. Store a separate presence marker when a legitimate value could be confused with absence.

For a large key space, a hash function maps each key to a smaller bucket index. A collision occurs when different keys reach the same bucket. The table must still compare keys; equal hashes do not establish equality.

Suppose the illustrative rule is integer_key mod 5. Keys 7 and 12 both reach bucket 2. A lookup for 12 must distinguish it from 7. Such a simple rule explains collisions but is not a general recommendation for handling arbitrary or adversarial keys.

Try this: place 4, 9, and 11 in five buckets. Which lookup needs more than the bucket address?

Practice: [705. Design HashSet](https://leetcode.com/problems/design-hashset/) and [706. Design HashMap](https://leetcode.com/problems/design-hashmap/).

## 6.2 Chaining, probing, and deletion

Separate chaining keeps a collection of key-value pairs in each bucket. Search that collection for the exact key. With n keys and m buckets, the load factor is α = n/m. A suitable random hash distribution gives expected O(1 + α) search; one long chain still takes O(n).

Open addressing keeps entries in the table itself. When a slot is occupied, a probe rule chooses another. Linear probing checks nearby slots; double hashing uses a second hash to choose a step. Probe rules must reach the needed slots. Open-addressed tables need unused capacity, and crowded tables can require many probes.

Deletion must preserve the search path. If two colliding keys occupy slots 2 and 3, clearing slot 2 as if it had never been used can make a search stop before reaching slot 3. A deleted marker lets searches continue. Rebuilding removes accumulated markers and redistributes entries.

Try this: insert keys hashing to slot 1 three times, then delete the middle entry. Complete a lookup for the last key.

Practice: [706. Design HashMap](https://leetcode.com/problems/design-hashmap/). Implement a small collision-heavy table locally before optimizing.

## 6.3 Hash functions, growth, and ordered lookup

A useful hash spreads keys across buckets and is consistent for equal keys. Universal hashing chooses a function at random from a family whose collision probability for any two fixed distinct keys is bounded. This gives a mathematical expectation under the family's assumptions; it is not a promise that every function choice avoids long chains.

Resizing allocates a larger table and places entries again because bucket indices depend on capacity. That resize costs O(n), so insertion claims often combine expected lookup behavior with amortized growth. These two qualifications explain different costs.

Hash tables support equality lookup well. They do not directly provide sorted order, predecessor, successor, or range queries. A balanced search tree supports those operations in O(log n) for basic updates and searches. A sorted array gives O(log n) search but O(n) insertion. Python dictionary insertion order is not sorted key order.

Try this: choose a structure for exact username lookup and another for listing timestamps within a range. Explain the operations each needs.

Practice: [49. Group Anagrams](https://leetcode.com/problems/group-anagrams/) and [1. Two Sum](https://leetcode.com/problems/two-sum/).

## 6.4 Frequency tables and indexes

A frequency table increments a count for each key. A reverse index maps a term to the documents or positions containing it. A sparse vector stores only nonzero entries, so a dot product can visit the smaller set of stored indices and look up matching entries in the other vector.

For a pair-sum scan over [6, 1, 8] with target 9, first ask whether 3 has appeared before storing 6. Then ask whether 8 appeared before storing 1. At 8, the needed 1 is already present. Looking before inserting prevents using the current position twice.

Expected time is O(n) if hash operations and key processing are bounded as assumed. For long string keys, computing hashes or comparing equal prefixes can itself cost time; count that work when it matters.

Try this: count words in "red blue red" and then subtract one occurrence of red. Decide whether zero counts should remain in the table.

Practice: [383. Ransom Note](https://leetcode.com/problems/ransom-note/) and [347. Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/).

## Review

Explain collisions, the load factor, and why deletion in a probing table needs care. Later, solve a new counting problem and compare a dictionary with sorting the keys.
