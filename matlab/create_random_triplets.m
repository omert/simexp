function create_random_triplets(ids, n, filename)

num_obj = length(ids);

ids = ids(:);
I = repmat(ids, ceil(2 * n / num_obj), 1);
M = [I I(randperm(length(I))) I(randperm(length(I)))];
M = unique(M, 'rows');
reps = find(M(:, 1) == M(:, 2) | M(:, 1) == M(:, 3) | M(:, 2) == M(:, 3));
M(reps, :) = [];
M = M(randperm(length(M)), :);
M = M(1:(min(n, length(M))), :);

f = fopen(filename, 'w');
for i = 1:n
    fprintf(f, '%d %d %d\n', M(i, 1), M(i, 2), M(i, 3));
end
fclose(f);
type(filename);


