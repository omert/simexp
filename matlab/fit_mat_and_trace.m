function [x S] = fit_mat_and_trace(IX, IA, IB, N, ids, iter, ...
                                         S)

if nargin < 6
    iter = 6;
end

n = length(ids);

if nargin < 7
    S = eye(n);
end

options = optimset('maxfunevals', 6, 'display', 'off');
trace_norm = fminbnd(@(tn) fit_mat_and_test(IX, IA, IB, N, ids, 2, ...
                                            S, tn), 0, 4, options);
fprintf(1, 'optimal trace norm: %f\n', trace_norm);
S = fit_mat(IX, IA, IB, N, ids, iter, S, trace_norm);


[U sig temp2] = svds(S, rank(S));
x = U * sqrt(sig);