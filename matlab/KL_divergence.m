function D = KL_divergence(P, Q)

D = sum(P .* log(P ./ Q  + eps), 2);