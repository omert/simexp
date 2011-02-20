function [x S] = fit_mat(IX, IA, IB, N, ids, iter, trace_norm, S)
%load(filename)

if nargin < 6
    iter = 6;
end

n = length(ids);

%fprintf(1, 'have %d objects and %d triplet\n', n, length(IX));

freedom_bound =  trace_norm * n;

if nargin < 8
    S = eye(n);
end

options = optimset('maxfunevals', 5, 'display', 'off');

S = projectPSD_norm(S, freedom_bound, 0);

T = S;

max_mu = 10;

num_no_improve = 0;
last_L = mat_model_likelihood(S, IX, IA, IB, N);
mu = 1;
for i = 1:iter
    %dS = update_matrix(S, IX, IA, IB, N);
    %dS = logistic_deriv(S, IX, IA, IB, N);
    dS = distance_deriv(S, IX, IA, IB, N);
    %deriv_norm = norm(S - projectPSD_norm(S + dS, freedom_bound));
    %    fprintf(1, 'convergence: %f\n', deriv_norm);
    
    %mu = fminbnd(@(mu) mat_model_likelihood(projectPSD_norm(S + mu ...
    %                                                  * dS, ...
    %                                                  freedom_bound), ...
    %                                        IX, IA, IB, N), 0, max_mu, ...
    %             options);
    %mu = 1 / sqrt(i);
    %max_mu = mu * 2;
    T = S + mu * dS;
    
    [S norm_iters] = projectPSD_norm(T, freedom_bound);
    [L percent_right eL] = mat_model_likelihood(S, IX, IA, IB, N);
    if L > last_L - 0.001 * mu
        num_no_improve = num_no_improve + 1;
        fprintf('small improvement\n');
    else
        num_no_improve = 0;
    end
    last_L = min(L, last_L);
    fprintf(1, '%d: mu: %f    L: %f   percent right: %f\n', i, mu, ...
            L, percent_right);

    if num_no_improve > 3
        break;
    end


    if norm_iters > 10
        %        mu = mu / 1.5;
    end
    if norm_iters < 5
        %        mu = mu * 1.5;
    end
end

[U sig temp2] = svds(S, rank(S));
x = U * sqrt(sig);