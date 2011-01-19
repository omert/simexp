function M1 = projectPSD_eig(M, max_eig)

% Project to positive semidefinites. M assumed to be symmetric
M = (M + M')/2;
[V D] = eig(M);

d = diag(D);
d = max(d, 0);
d = min(d, max_eig);
D = diag(d);

M1 = V * D * V';
M1 = (M1 + M1')/2;
