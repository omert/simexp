function [ibest, jbest] = approx_best_paired_comp(x, I0, J0, N0, prior0, exclusions, n)

[num_obj d] = size(x);

I = zeros(n * 250, 1);
J = zeros(n * 250, 1);
sample_dist = prior0';
fprintf('checking %d pairs\n', length(I));
sample_dist(exclusions) = 1e-100;
for i = 1:length(I)
    pair = sample_from_dist(sample_dist, 2);
    I(i) = pair(1);
    J(i) = pair(2);
end


uncond_prob = paired_comp_prob(x, x, I, J);
N = ones(size(I));

LL = -paired_comp_llh(x, x, I0, J0, N0) + log(prior0);
prior = conditional_prob_from_ll(LL);
 
uncond_prob = uncond_prob.^ repmat(N, 1, num_obj);
p_prior = uncond_prob * prior';
prior = repmat(prior, length(I), 1);
LL = repmat(LL, length(I), 1);
LL1 = log(uncond_prob) + LL;
LL2 = log(1 - uncond_prob) + LL;
post1 = conditional_prob_from_ll(LL1);
post2 = conditional_prob_from_ll(LL2);
    
kldiv = p_prior .* KL_divergence(post1, prior) + (1 - p_prior) .* KL_divergence(post2, prior);
[~, iinfo] = sort(kldiv, 'descend');
ibest = I(iinfo(1:n));
jbest = J(iinfo(1:n));


