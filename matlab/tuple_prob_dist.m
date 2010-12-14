function P = tuple_prob_dist(beta, X, I)

B = repmat(beta, length(I), 1);
LLH = -log(1 + sum((B - X(I(:), :)).^2, 2));
P = normalize_dist(exp(LLH));


