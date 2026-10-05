# 17. Number theory and bit operations

Integer algorithms use divisibility, remainders, and binary representation. When integers grow large, the cost of arithmetic depends on their number of bits.

## 17.1 Divisibility and greatest common divisors

An integer a divides b when b = ak for some integer k. A prime is an integer greater than 1 with no positive divisors except 1 and itself. Every integer greater than 1 has a unique prime factorization up to order.

The greatest common divisor, gcd(a, b), is the largest positive integer dividing both, when a and b are not both zero. Euclid's algorithm repeatedly replaces (a, b) with (b, a mod b) until the second value is zero. The common divisors stay the same because a = qb + r.

For 30 and 18, the pairs are (30, 18), (18, 12), (12, 6), (6, 0), so the gcd is 6. Extended Euclid also finds coefficients x and y with ax + by = gcd(a, b). Here -1×30 + 2×18 = 6.

Try this: complete gcd(35, 15), then verify coefficients -1 and 3. Euclid takes O(log min(a, b)) divisions for positive inputs, but large-integer division is not constant time.

Practice: [1979. Find Greatest Common Divisor of Array](https://leetcode.com/problems/find-greatest-common-divisor-of-array/).

## 17.2 Modular equations and inverses

Working modulo m treats numbers with the same remainder as equivalent. Addition and multiplication preserve this equivalence. Division needs an inverse: a number a has a multiplicative inverse modulo m exactly when gcd(a, m) = 1.

For 3 modulo 7, the inverse is 5 because 3×5 = 15 leaves remainder 1. Therefore 3x ≡ 2 mod 7 gives x ≡ 10 ≡ 3. Extended Euclid supplies inverses when they exist.

More generally, ax ≡ b mod m has solutions exactly when gcd(a, m) divides b. Dividing all three values by that gcd produces an equation with an invertible coefficient, then lifts to the corresponding residue classes.

The Chinese remainder theorem combines congruences with pairwise coprime moduli into one residue modulo their product. For x ≡ 1 mod 3 and x ≡ 2 mod 5, x ≡ 7 mod 15. Noncoprime moduli require compatible residues and a more general formulation.

Try this: does 4x ≡ 3 mod 6 have a solution? No, since gcd(4, 6) = 2 does not divide 3.

Practice: [1497. Check If Array Pairs Are Divisible by k](https://leetcode.com/problems/check-if-array-pairs-are-divisible-by-k/). It practices remainder classes; solve the inverse and CRT examples separately.

## 17.3 Fast powers and primality

Repeated squaring computes a^e in O(log e) multiplications. Keep an accumulated result and a current base. For each binary exponent bit, multiply the result by the base when the bit is 1, square the base, and shift the exponent. Reduce modulo m after every multiplication when computing modular powers.

For 3^5 mod 7, 5 has bits 101. The needed factors are 3 and 3^4; since 3² ≡ 2 and 3⁴ ≡ 4, the result is 3×4 ≡ 5.

Trial division tests possible factors through √n. A sieve marks multiples to find many primes up to a limit, using O(N log log N) time in the standard sieve analysis. Fermat's congruence is useful but not a complete primality test: some composite numbers pass. Miller–Rabin writes n - 1 = 2^s d with d odd and checks modular powers for witnesses of compositeness. For an odd composite, independently uniform suitable bases give a false-prime probability at most 4^-k after k rounds; specific deterministic base sets need a stated integer range.

Try this: trace the exponent bits for 2^13 and count squarings instead of multiplying thirteen copies.

Practice: [50. Pow(x, n)](https://leetcode.com/problems/powx-n/) and [204. Count Primes](https://leetcode.com/problems/count-primes/).

## 17.4 RSA as an arithmetic application

RSA links modular powers with a composite modulus. In a small mathematical example, choose primes p = 5 and q = 11, so n = 55 and φ(n) = 40. Choose e = 3, coprime to 40, and d = 27 because 3×27 ≡ 1 mod 40.

For message m = 2, the arithmetic encryption is c = m^e mod n = 8. Raising 8 to d modulo 55 recovers 2. The exponent relation, prime-modulus arithmetic, and the Chinese remainder theorem explain why recovery works for residues modulo n.

The public values are n and e; factoring n reveals enough information to derive the private exponent in this construction. The toy numbers and bare exponentiation are educational only. Real encryption requires a vetted scheme with appropriate padding and key generation; raw textbook RSA is not a secure message format.

Try this: verify e×d mod 40 and compute 2³ mod 55. Use repeated squaring for the reverse step.

Practice: [372. Super Pow](https://leetcode.com/problems/super-pow/) practices modular exponentiation, not secure cryptographic implementation.

## 17.5 Bit masks and subset enumeration

A bit mask uses individual binary positions to represent membership or flags. AND keeps bits set in both operands; OR keeps bits set in either; XOR keeps bits that differ. Shifts move bit positions.

For mask 1010, clearing its lowest set bit gives mask & (mask - 1) = 1000. Repeating this once per set bit counts selected items. To enumerate all subsets of n items, iterate masks from 0 through 2^n - 1 and test bit i for item i.

Fixed-width machines can overflow and distinguish signed from unsigned shifts. Python integers grow as needed and bitwise operations on negative numbers behave as if there were infinitely many leading sign bits. Specify a width and mask when a problem expects, for example, exactly 32 bits.

Try this: enumerate the submasks of 101: 101, 100, 001, 000. The update (sub - 1) & mask needs a separate stop at zero.

Practice: [191. Number of 1 Bits](https://leetcode.com/problems/number-of-1-bits/) and [136. Single Number](https://leetcode.com/problems/single-number/).

## Review

Explain why modular division requires an inverse and why a fast exponentiation bound counts multiplications rather than bit-level work. Reconstruct Euclid's steps on new numbers in a later session.
