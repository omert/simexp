function [llh g H] = paired_comp_llh(beta, X, I, J, N)

[num_obj d] = size(X);
if isempty(I)
    beta_size = size(beta);
    num_vecs = beta_size(1);
    llh = -log(ones(1, num_vecs) / num_vecs);
    return
end
P = paired_comp_prob(beta, X, I, J);
llh = -sum(repmat(N, 1, num_obj) .* log(P), 1);


