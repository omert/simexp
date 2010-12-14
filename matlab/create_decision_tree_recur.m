function create_decision_tree_recur(choice_path, prior, f, x, degree, depth, ids, last, cutoff)

if isempty(last)
    last = 1;
end

Iprior = find(prior >= max(prior) * cutoff);

if length(choice_path) > depth || length(Iprior) < degree
    if length(choice_path) == depth + 1
        p = choice_path(1:(end-1));
        iters = sum(p + (p - 1) .* degree.^(depth:-1:1));
        iters_total = sum(2 * degree + (degree - 1) .* degree.^(depth:-1:1));
        t = toc / iters * (iters_total - iters);
        ttotal = toc / iters * iters_total;
        fprintf('expected time to finish: %.0f seconds. estimated total: %.0f seconds\n', t, ttotal);
    end
    
    D = sum((x - repmat(x(last, :), length(x), 1)).^2, 2);
    [~, I] = sort(D);
    fprintf(f, '%d ', choice_path);
    fprintf(f, ': ');
    fprintf(f, '%d ', ids(I(1:degree)));
    fprintf(f, '\n');
    
    return
end


fprintf('path: ');
fprintf('%d ', choice_path);
fprintf('\n  exp entropy of prior: %.4f\n', exp(entropy(prior, 1)));



I = find(prior < max(prior) * cutoff);
sample_prior = prior;
sample_prior(I) = sample_prior(I) * 1e-20;
sample_prior(last) = sample_prior(last) * 1e-20;
sample_prior = normalize_dist(sample_prior);
sample = [last; randsample(length(prior), degree - 1, true, sample_prior)];

best_kl_div = 0;
best_tuple = [];
best_posts = [];
num_tries = 150;
for i = 1:num_tries
    P = zeros(length(x), degree);
    for j = 1:length(x)
        P(j, :) = tuple_prob_dist(x(j, :), x, sample)';
    end
    posts = normalize_dist(P .* repmat(prior, 1, degree), 1);
    Pchoice = P' * prior;
    KL = KL_divergence(posts', repmat(prior', degree, 1));
    kldiv = Pchoice' * KL;
    if kldiv > best_kl_div
        best_kl_div = kldiv;
        best_tuple = sample;
        best_posts = posts;
    else
        sample = best_tuple;
    end
    iswap = ceil(rand * (degree - 1)) + 1;

    sample_prior = prior;
    I = [find(prior < max(prior) / cutoff); sample];
    sample_prior(I) = sample_prior(I) * 1e-20;
    sample_prior = normalize_dist(sample_prior);

    iswapee = randsample(length(prior), 1, true, sample_prior);
    sample(iswap) = iswapee;
end
fprintf('  KL divergence in bits: %.3f\n', best_kl_div / log(2));

tuple = ids(best_tuple);

fprintf(f, '%d ', choice_path);
fprintf(f, ': ');
fprintf(f, '%d ', tuple);
fprintf(f, '\n');


for i = 1:degree
    new_path = [choice_path i];
    create_decision_tree_recur(new_path, best_posts(:, i), f, x, degree, depth, ids, best_tuple(i), cutoff)
end

    
    
