# 15. Regular expressions and compression

A regular expression describes a family of strings. Compression represents data with fewer bits by exploiting unequal frequencies or repeated structure. Both depend on precise rules for interpreting the representation.

## 15.1 Regular languages and automata

Concatenation means one pattern followed by another. Alternation chooses between patterns. Repetition allows a pattern to occur multiple times. For example, a(b|c)* matches an a followed by zero or more b or c characters.

A nondeterministic finite automaton, or NFA, may have several possible states after reading a character. It can also have empty, or epsilon, transitions that consume no character. To simulate it, first follow all reachable epsilon transitions, then consume one character across every matching transition, then take epsilon closure again.

Tracking a set of states avoids exploring identical possibilities repeatedly. For a straightforward regex NFA with O(m) states and edges, scanning n characters takes O(mn) time and O(m) active-state space. Backtracking regex engines behave differently and can take exponential time on some patterns. Features such as backreferences exceed ordinary finite-automaton matching.

Try this: list the active possibilities after reading "ab" for a(b|c)*. Why does the empty repetition also allow "a"?

Practice: [10. Regular Expression Matching](https://leetcode.com/problems/regular-expression-matching/). Its supported syntax is narrower than a full regex language; define the meaning of dot and star from that problem before solving.

## 15.2 Bits, run-length encoding, and prefix codes

Lossless compression lets a decoder reconstruct the original data exactly. Not every input can become shorter: there are fewer short bit strings than all possible longer inputs. A useful compressor takes advantage of recurring structure in likely data and includes enough information to decode it.

Run-length encoding stores repeated values and their lengths. "aaaaabb" becomes five a characters and two b characters. It is compact for long runs but can grow alternating input. The encoding must distinguish counts from literal data and specify how long counts are represented.

Prefix codes assign variable-length bit strings to symbols without making one code a prefix of another. With A = 0, B = 10, C = 11, the bits 01011 decode unambiguously to ABC. An end marker or known output length tells the decoder when to stop.

Try this: decode 11010 using those codes. It is CAB. Compare encoded size with a fixed-width representation and include any code-table overhead.

Practice: [443. String Compression](https://leetcode.com/problems/string-compression/). Its in-place character format practices runs, not a general binary compression format.

## 15.3 Huffman encoding and decoding

Huffman coding builds a prefix tree by merging the least frequent remaining nodes. To encode a symbol, follow its leaf path from the root and write the edge bits. To decode, follow bits until reaching a leaf, emit its symbol, then return to the root.

For frequencies A = 6, B = 2, C = 1, merge B and C, then their combined node with A. One valid code is A = 0, B = 10, C = 11. Average payload length is (6×1 + 2×2 + 1×2)/9 = 4/3 bits per symbol. A real file also needs a code description and a length or end rule.

Frequency counting scans the input. Tree construction costs O(k log k) for k distinct symbols. Encoding and decoding then scale with input characters and emitted or consumed bits. The single-symbol case needs a convention so repeated occurrences remain decodable.

Try this: encode ACBA, then decode the result without referring to the letters. The bit string is 011100 with the code above.

Practice: [1167. Minimum Cost to Connect Sticks](https://leetcode.com/problems/minimum-cost-to-connect-sticks/) practices the merge order, not the codec, and may require a subscription. Independently round-trip a short message to test encoding and decoding.

## 15.4 Dictionary compression and LZW

Dictionary compression replaces recurring sequences with references. LZW begins with a dictionary of single symbols. The encoder finds the longest current dictionary phrase matching the upcoming text, emits its code, and adds that phrase plus the next character as a new entry.

Suppose the initial symbols are A and B. Reading "ABABABA" first emits A and adds AB; then emits B and adds BA; then emits AB and adds ABA. Later occurrences can use longer phrases. The decoder rebuilds the same dictionary from previously decoded phrases, so the growing dictionary need not be transmitted entry by entry.

There is one special case: a code can refer to the phrase the decoder is about to create. Then the phrase is previous_phrase + its first character. Bit width, dictionary capacity, and reset behavior must match between encoder and decoder. Runtime depends on dictionary lookup and phrase handling; repeatedly copying long strings can dominate a naive implementation.

Try this: continue the example after emitting AB. Check each emitted code against the dictionary available at that moment.

Practice: [535. Encode and Decode TinyURL](https://leetcode.com/problems/encode-and-decode-tinyurl/) is related identifier-dictionary practice, not LZW compression. For LZW itself, implement an original two-symbol encoder/decoder and test the repeated-phrase special case.

## Review

Explain why unambiguous decoding needs more than short codes. Later, compare runs, Huffman frequencies, and repeated phrases on a new string and predict which kind of structure each can exploit.
