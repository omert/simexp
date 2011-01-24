function M1 = projectPSD_norm(M, max_trace)

% Project to positive semidefinites. M assumed to be symmetric

n = length(M);
M = M + (max_trace * eye(n) - M .* eye(n));

M = (M + M')/2;
[V D] = eig(M);

D = max(D, 0);
M1 = V * D * V';
M1 = (M1 + M1')/2;

