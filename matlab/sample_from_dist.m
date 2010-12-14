function sample = sample_from_dist(P, n)
% no repetitions

sample = zeros(1, n);
for i=1:n
    C = cumsum(P);
    r = rand;
    [~, I] = sort([r; C]);
    sample(i) = min(find(I == 1), length(P));
    P(sample(i)) = 1e-100;
    P = normalize_dist(P);
end

