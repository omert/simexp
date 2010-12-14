function [imax, p, kldiv] = best_guess_kl_div(x, I, J, N, prior0)

LL = -paired_comp_llh(x, x, I, J, N) + log(prior0);
prior = conditional_prob_from_ll(LL);


[p, imax] = max(prior);
post1 = zeros(size(prior));
post1(imax) = 1;
post2 = prior;
post2(imax) = 0;
post2 = post2 / sum(post2);
kldiv = p * KL_divergence(post1, prior) + (1 - p) * KL_divergence(post2, prior);