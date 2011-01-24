function M1 = projectPSD_norm(M, max_trace)

% Project to positive semidefinites. M assumed to be symmetric


M = (M + M')/2;
[V D] = eig(M);

D = max(D, 0);
M1 = V * D * V';
M1 = (M1 + M1')/2;

d = min(1.0, sqrt(max_trace / length(M) ./ (1e-10 + diag(M1))));
for i = 1:length(M1);
    M1(:, i) = M1(:, i) * d(i);
    M1(i, :) = M1(i, :) * d(i);
end
