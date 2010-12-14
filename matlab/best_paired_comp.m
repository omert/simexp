function [ibest, jbest, pbest, kldiv] = best_paired_comp(x, I0, J0, N0, prior0, exclusions, manual)


[num_obj d] = size(x);

persistent Iall Jall uncond_prob_all x_norm
if isempty(x_norm) || x_norm ~= norm(x)
    Iall = 1:num_obj;
    Jall = 1:num_obj;
    [Iall Jall] = meshgrid(Iall, Jall);
    K = find(Iall > Jall);
    Iall = Iall(K);
    Iall = Iall(:);
    Jall = Jall(K);
    Jall = Jall(:);

    x_norm = norm(x);
    uncond_prob_all = paired_comp_prob(x, x, Iall, Jall);
    
end



if manual
    IJ = [Iall Jall];
    IJ0 = [I0(:) J0(:)];
    [~, K] = setdiff(IJ, IJ0, 'rows');
    I = Iall(K);
    J = Jall(K);
    uncond_prob = uncond_prob_all(K, :);
end

K = find(ismember(I, exclusions) | ismember(J, exclusions));
I(K) = [];
J(K) = [];
uncond_prob(K, :) = [];


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
if manual
    for i=1:length(I)
        post1(i, I(i)) = 1e-100;
        post2(i, I(i)) = 1e-100;
        post1(i, J(i)) = 1e-100;
        post2(i, J(i)) = 1e-100;
    end
    post1 = post1 ./ repmat(sum(post1, 2), 1, length(x));
    post2 = post2 ./ repmat(sum(post2, 2), 1, length(x));
end
    
kldiv = p_prior .* KL_divergence(post1, prior) + (1 - p_prior) .* KL_divergence(post2, prior);
[kldiv, iinfo] = max(kldiv);
ibest = I(iinfo);
jbest = J(iinfo);
pbest = p_prior(iinfo);

