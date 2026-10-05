# 16. Matrices, linear programming, and FFT

Numerical algorithms use algebraic structure to reduce work. Floating-point calculations also require attention to rounding and to how sensitive a problem is to small input changes.

## 16.1 Matrix multiplication and Strassen's idea

If A has dimensions p×q and B has dimensions q×r, their product has dimensions p×r. Entry (i, j) is the dot product of row i and column j. The direct method performs Θ(pqr) arithmetic operations.

For A = [[1, 2], [3, 4]] and B = [[2, 0], [1, 5]], the top-left entry is 1×2 + 2×1 = 4. Complete the other entries: the product is [[4, 10], [10, 20]]. Matrix multiplication is associative but generally not commutative. The identity matrix leaves a compatible matrix unchanged; transposing a product reverses factor order: (AB)ᵀ = BᵀAᵀ.

Splitting square matrices into four blocks leads to eight recursive half-size products, giving T(n) = 8T(n/2) + O(n²) = O(n³). Strassen's method combines block sums and differences so only seven recursive products are needed. For blocks a,b,c,d and e,f,g,h, one product is (a+d)(e+h); six other combinations let the four output blocks be recovered by additions. Its recurrence gives O(n^(log₂7)), about O(n^2.807). Padding, extra memory, numerical behavior, and constants affect practical usefulness.

Try this: count scalar multiplications for the direct two-by-two product, then explain why seven recursive products change the exponent.

Practice: [48. Rotate Image](https://leetcode.com/problems/rotate-image/) practices matrix indexing only. Implement a direct two-by-two product separately before studying fast multiplication.

## 16.2 Linear systems, inversion, and least squares

A linear system Ax = b asks for unknown values x that satisfy several linear equations. Gaussian elimination combines rows to remove variables, producing a triangular system solved by substitution. Pivoting exchanges rows to choose a usable pivot and can improve numerical behavior.

For x + y = 5 and 2x + 3y = 12, subtract twice the first equation from the second: y = 2, then x = 3. A zero pivot does not automatically mean no solution; another row may supply a pivot, or the system may have dependent equations. Rank and consistency determine whether solutions are unique, absent, or nonunique.

Factoring a dense matrix into triangular factors takes O(n³) arithmetic work; each new right-hand side can then be solved in O(n²). Inversion solves against identity columns, but explicitly forming an inverse is often unnecessary. Symmetric positive-definite matrices allow Cholesky factorization A = LLᵀ.

Least squares minimizes ||Ax - b||² when exact agreement is impossible. The normal equations are AᵀAx = Aᵀb. With independent columns they have a unique solution, but forming AᵀA can worsen conditioning; QR methods avoid that squaring of the condition number.

Try this: fit one constant to observations 2 and 6. Minimizing squared error gives 4.

Practice: [640. Solve the Equation](https://leetcode.com/problems/solve-the-equation/) practices equation manipulation in one variable. Separately solve the two-equation system to practice elimination.

## 16.3 Linear programming and duality

Linear programming optimizes a linear objective subject to linear inequalities. The feasible region is the set satisfying every constraint. A problem can be infeasible, have a finite optimum, or be unbounded.

Maximize 3x + 2y subject to x + y ≤ 4, x ≤ 2, and x,y ≥ 0. The corner (2, 2) gives 10; (0, 4) gives 8 and (2, 0) gives 6. For this bounded polygon, checking corners finds an optimum. In higher dimensions, algorithms exploit structure instead of enumerating every vertex.

Simplex moves among feasible corner representations and is often effective, but has exponential worst cases. Polynomial-time approaches include ellipsoid and interior-point methods, under their respective arithmetic and precision models.

Duality supplies bounds. Multiplying x + y ≤ 4 by 2 and x ≤ 2 by 1 yields 3x + 2y ≤ 10. A feasible point reaching 10 proves optimality. More generally, feasible dual variables combine constraints into an objective bound; when finite feasible optima exist, primal and dual optimal values agree.

Try this: show why (3, 1) is not feasible even though its objective is 11.

Practice: [134. Gas Station](https://leetcode.com/problems/gas-station/) is related feasibility reasoning only. It is not a linear-programming solver exercise; independently derive the bound above and vary one constraint.

## 16.4 Polynomials, convolution, and FFT

A polynomial can be stored by coefficients or by its values at enough distinct points. Multiplying coefficient lists directly requires combining every pair. For (1 + 2x)(3 + x), the coefficients are [3, 7, 2]. This operation on coefficient sequences is convolution.

In point-value form, multiplication is easy: multiply corresponding values. The fast Fourier transform, or FFT, efficiently converts between coefficients and values at specially chosen complex roots of unity. Split coefficients into even and odd positions; both smaller transforms reuse the same structure. Combine their answers with paired sums and differences called butterflies.

A transform of length N uses O(N log N) arithmetic operations. To multiply lengths a and b without wraparound, pad to a transform length at least a + b - 1, often a power of two. Transform both arrays, multiply values pointwise, inverse-transform, and normalize by N. Floating-point error requires care when recovering integer coefficients; number-theoretic transforms use compatible modular roots instead.

FFT circuits arrange independent butterflies in layers. There are O(log N) layers and O(N log N) total arithmetic work, exposing parallelism.

Try this: multiply coefficient lists [2, 1] and [1, 3] directly. The result is [2, 7, 3]; use it to check a later FFT implementation.

Practice: [43. Multiply Strings](https://leetcode.com/problems/multiply-strings/) practices digit convolution and carries. Its ordinary constraints do not require FFT.

## 16.5 Rank and invertibility

The rank of a matrix is the number of independent columns, equivalently independent rows. Dependent columns repeat information: one can be formed by combining others. A square matrix has an inverse exactly when its rank equals its dimension.

For [[1, 2], [2, 4]], the second row is twice the first. The equations x + 2y = 3 and 2x + 4y = 6 describe the same line, so there are infinitely many solutions. Changing the second right-hand side to 7 makes them inconsistent. The matrix itself remains singular in both cases.

For a two-by-two matrix [[a, b], [c, d]], the determinant is ad - bc. A zero determinant signals singularity. If it is nonzero, the inverse is [[d, -b], [-c, a]] divided by the determinant. Higher-dimensional determinants describe signed volume scaling, but solving a large system by determinant formulas is usually inefficient compared with factorization.

A symmetric matrix equals its transpose. Positive definiteness means xᵀAx > 0 for every nonzero real vector x. This stronger condition gives a unique minimum for the associated quadratic objective and supports Cholesky factorization. A nearly singular matrix can make an answer highly sensitive to tiny input changes, even when an inverse formally exists.

Try this: compute the determinant of [[2, 1], [1, 2]]. It is 3. Multiply the proposed inverse by the original matrix to check that the result is the identity.

Practice: [73. Set Matrix Zeroes](https://leetcode.com/problems/set-matrix-zeroes/) practices matrix traversal only. Use the original inverse check above for the algebra; LeetCode does not supply the full linear-algebra exercise sequence.

## Review

Separate algebraic operation counts from numerical accuracy. Later, compute one matrix product, derive one linear-programming upper bound, and multiply two short coefficient lists without notes.
