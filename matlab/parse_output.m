function [IX, IA, IB, N, ids] = parse_output(filename, dataset)

[I J K T] = textread(filename, '%d %d %d %f');
fprintf('found %d comparisons\n', length(I));
Iunique = find(I ~= J & I ~= K & J ~= K);
I = I(Iunique);
J = J(Iunique);
K = K(Iunique);
ids = unique([I; J; K]);
inv_ids = zeros(length(ids), 1);
inv_ids(ids + 1) = 1:length(ids);
I = inv_ids(I + 1);
J = inv_ids(J + 1);
K = inv_ids(K + 1);
M = sortrows([I J K]);
I = M(:, 1);
J = M(:, 2);
K = M(:, 3);
Ishift = [I(2:end); -1];
Jshift = [J(2:end); -1];
Kshift = [K(2:end); -1];
IJKdiff = (I == Ishift & J == Jshift & K == Kshift);
Inew = find(IJKdiff == 0);
N = (1:length(I))';
IX = I(Inew);
IA = J(Inew);
IB = K(Inew);
N = diff([0; N(Inew)]);

x = randn(length(ids), 3);
save_experiement_data([filename '.data.mat'], IX, IA, IB, N, ids, dataset, x);


  