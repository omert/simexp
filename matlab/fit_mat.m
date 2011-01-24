function [x S] = fit_mat(IX, IA, IB, N, ids, iter, trace_norm)
%load(filename)

if nargin < 6
    iter = 6;
end

n = length(ids);

%fprintf(1, 'have %d objects and %d triplet\n', n, length(IX));

freedom_bound =  trace_norm;

S = eye(n);

options = optimset('maxfunevals', 5, 'display', 'off');

L = mat_model_likelihood(S, IX, IA, IB, N);
%fprintf(1, 'initial likelihood: %f\n', L);
S = projectPSD_norm(S, freedom_bound);
L = mat_model_likelihood(S, IX, IA, IB, N);
%fprintf(1, 'likelihood after projection: %f\n', L);

max_mu = 10;

for i = 1:iter
    %S1 = update_matrix(S, IX, IA, IB, N);
    S1 = logistic_deriv(S, IX, IA, IB, N);
    %S1 = distance_deriv(S, IX, IA, IB, N);
    deriv_norm = norm(S - projectPSD_norm(S + S1, freedom_bound));
    %    fprintf(1, 'convergence: %f\n', deriv_norm);
    
    %mu = fminbnd(@(mu) mat_model_likelihood(projectPSD_norm(S + mu ...
    %                                                  * S1, ...
    %                                                  freedom_bound), ...
    %                                        IX, IA, IB, N), 0, max_mu, ...
    %             options);
    mu = 1 / sqrt(i);
    max_mu = min(mu * 2, 1);
    S = projectPSD_norm(S + mu * S1, freedom_bound);
    max(diag(S))
    [L percent_right eL] = mat_model_likelihood(S, IX, IA, IB, N);
    fprintf(1, ' mu: %f    L: %f   percent right: %f\n', mu, L, ...
            percent_right);
    %    fprintf(1, 'expected L: %f \n', eL);
    if mu < 0.001 | deriv_norm < 0.1
        break;
    end
end

[U sig temp2] = svds(S, rank(S));
x = U * sqrt(sig);