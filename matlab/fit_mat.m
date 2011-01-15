function [x fit_val] = fit_mat(IX, IA, IB, N, ids, iter)
%load(filename)

if nargin < 6
    iter = 6;
end

n = length(ids);
x = ones(n, n);

for i = 1:iter
    x1 = update_matrix(x, IX, IA, IB, N);
    x = projectPSD(x + x1);
    model_likelihood(sqrtm(x), IX, IA, IB, N)
end
