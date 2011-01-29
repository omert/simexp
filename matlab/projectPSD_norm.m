function [M1 iter] = projectPSD_norm(M, max_trace, recalc_d)

% Project to positive semidefinites. M assumed to be symmetric

persistent d;

M = (M + M')/2;
n = length(M);
max_norm = max_trace / n;

max_err = 0.01;

if length(d) ~= n || nargin >= 3
    d = max_norm - diag(M);
    fprintf('producing new diagonal\n');
end

for iter = 1:500
    M1 = projectPSD(M + diag(d));
    dm1 = diag(M1);
    d = d + max_norm - dm1;
    er = max(abs(dm1 - max_norm));
    if er < max_err * max_norm
        break;
    end
end
fprintf('projectPSD_norm iterations: %d\n', iter);


