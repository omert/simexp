function [S fit_val] = fit_mat(IX, IA, IB, N, ids, iter, S)
%load(filename)

if nargin < 6
    iter = 6;
end

n = length(ids);

freedom_bound =  2 * n;

if nargin < 7
    S = ones(n, n);
end

options = optimset('maxfunevals', 10, 'display', 'off');

L = mat_model_likelihood(S, IX, IA, IB, N);
fprintf(1, 'initial likelihood: %f\n', L);
S = projectPSD_trace(S, freedom_bound);
L = mat_model_likelihood(S, IX, IA, IB, N);
fprintf(1, 'likelihood after projection: %f\n', L);

for i = 1:iter
    %    S1 = update_matrix(S, IX, IA, IB, N);
    S1 = logistic_deriv(S, IX, IA, IB, N);
    mu = fminbnd(@(mu) mat_model_likelihood(projectPSD_trace(S + mu ...
                                                      * S1, freedom_bound), ...
                                            IX, IA, IB, N), 1, 10, options);
    S = projectPSD_trace(S + mu * S1, freedom_bound);
    L = mat_model_likelihood(S, IX, IA, IB, N);
    fprintf(1, 'mu: %f    L: %f\n', mu, L);
end
