function [x fit_val] = fit(x0, IX, IA, IB, N, iter)
%load(filename)

if nargin < 6
    iter = 6;
end

x = x0;
options = optimset('display', 'iter', 'maxfunevals', 1000000, 'GradObj','on', 'derivativecheck', 'off', 'maxiter', iter, 'tolfun', 0.001);
x = fminunc(@(x) model_likelihood(x, IX, IA, IB, N), x, options);
options = optimset('display', 'iter', 'maxfunevals', 1000000, 'GradObj','off', 'derivativecheck', 'off', 'maxiter', iter * 2, 'tolfun', 0.001);
[x, fit_val] = fminunc(@(x) model_likelihood(x, IX, IA, IB, N), x, options);




