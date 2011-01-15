function M1 = projectPSD(M)

% Project to positive semidefinites. M assumed to be symmetric

[V D] = eig(M);

D = max(D, 0);
M1 = V * D * V';