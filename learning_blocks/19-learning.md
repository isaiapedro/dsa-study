# 19. Clustering, weights, and gradient descent

Machine-learning algorithms use data to choose a model or a decision rule. Their guarantees depend on the objective and assumptions; computing an answer to an optimization problem does not by itself establish that the model describes the world well.

## 19.1 Clustering and distance

Clustering groups similar points. The distance measure defines similarity, and the objective defines what counts as a good grouping. Squared Euclidean distance, ordinary Euclidean distance, and an arbitrary dissimilarity table are not interchangeable.

In k-means, choose k centers, assign each point to its nearest center, then replace each center by the mean of its assigned points. Each assignment step and each mean update cannot increase the sum of squared distances. The process can settle at a local optimum, and the starting centers matter.

For points 0, 2, 9, and 11 with centers 0 and 9, assignments are {0, 2} and {9, 11}; updated centers are 1 and 10. Empty clusters need an explicit handling rule. A basic iteration costs O(nkd) for n points in d dimensions.

The k-center objective instead minimizes the largest distance to a chosen center. In a metric space, repeatedly choosing the point farthest from existing centers gives a factor-2 approximation. The selected far-apart points force an optimal solution with only k centers to place two of them in the same optimal group, bounding their separation by twice the optimal radius.

Try this: compute squared error before and after the mean update in the one-dimensional example. It decreases from 8 to 4.

Practice: [973. K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/) practices distance and selection, not clustering. Independently perform two k-means iterations to practice clustering itself.

## 19.2 Multiplicative weights

Multiplicative weights maintains a weight for each candidate strategy. After observing losses, reduce the influence of candidates that performed poorly, then normalize the weights to form a new distribution. Unlike choosing only the latest winner, it keeps several candidates in consideration.

One common update for losses in [0, 1] is w_i ← w_i exp(-η loss_i), with η > 0 controlling responsiveness. Starting from equal weights, a zero-loss candidate keeps its weight while a loss-1 candidate is multiplied by exp(-η). Small η changes preferences slowly; large η reacts more sharply.

For two candidates with equal initial weights and losses 0 and 1, using η = ln 2 changes weights to 1 and 1/2, then probabilities to 2/3 and 1/3. Repeated updates compare cumulative performance against a fixed candidate in hindsight. Regret bounds require the stated loss range, update rule, learning-rate choice, and evaluation model.

Try this: reverse the losses on the next round. The unnormalized weights become 1/2 and 1/2, restoring equal probability.

Practice: [528. Random Pick with Weight](https://leetcode.com/problems/random-pick-with-weight/) practices sampling from weights. It does not implement loss-based updates or prove a regret bound.

## 19.3 Gradient descent

A gradient lists how a function changes with each coordinate. Gradient descent moves opposite the gradient to reduce the objective: x_next = x - η∇f(x), where η is the step size.

For f(x) = (x - 3)², the derivative is 2(x - 3). Starting at x = 0 with η = 1/4 gives x = 1.5, then 2.25, then 2.625. The values approach the minimum at 3. A step that is too large can oscillate or diverge.

For smooth convex objectives, suitable step sizes give convergence guarantees toward a global minimum under the corresponding assumptions. Nonconvex objectives can have local minima and stationary points that are not global minima. A constrained problem may project each step back into the feasible set.

Stochastic gradient methods estimate the gradient from a sample or minibatch. Each step can be cheaper, but noise changes the analysis and stopping behavior. Feature scaling, arithmetic precision, and the stopping rule affect a practical implementation.

Try this: repeat the quadratic example with η = 1. The sequence alternates between 0 and 6 instead of converging.

Practice: [1515. Best Position for a Service Centre](https://leetcode.com/problems/best-position-for-a-service-centre/) is related continuous optimization. Its sum of distances is not differentiable at a data point, so the smooth quadratic update cannot be applied blindly.

## Review

State the objective before choosing a method. Later, distinguish a k-means mean update, a multiplicative weight update, and a gradient step using new numbers. Explain which assumptions make each guarantee possible.
