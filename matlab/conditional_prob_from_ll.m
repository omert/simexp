function P = conditional_prob_from_ll(LL)

sizeLL = size(LL);

LL = LL - repmat(max(LL, [], 2), 1, sizeLL(2));
P = exp(LL);
P = P ./ repmat(sum(P, 2), 1, sizeLL(2));
