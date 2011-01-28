function create_triplet_bank(ids, sample_size, num_per_obj, filename)

n = sample_size * num_per_obj;
num_obj = length(ids);
ids = ids(:);

I = randperm(length(ids));
sample_ids = ids(I(1:sample_size));


J = repmat(sample_ids, 2 * num_per_obj, 1);
I = repmat(ids, 2 * length(J) / length(ids), 1);
I = I(1:length(J));
M = [J I(randperm(length(I))) I(randperm(length(I)))];
M = unique(M, 'rows');
reps = find(M(:, 1) == M(:, 2) | M(:, 1) == M(:, 3) | M(:, 2) == M(:, 3));
M(reps, :) = [];
M = M(randperm(length(M)), :);
M = M(1:(min(n, length(M))), :);
whos
f = fopen(filename, 'w');
for i = 1:n
    fprintf(f, '%d %d %d\n', M(i, 1), M(i, 2), M(i, 3));
end
fclose(f);
type(filename);


