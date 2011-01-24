function [x S] = fit_mat_and_trace(IX, IA, IB, N, ids, iter)

if nargin < 6
    iter = 6;
end

n = length(ids);

if nargin < 7
    S = eye(n);
end

options = optimset('maxfunevals', 6, 'display', 'off');
trace_norm = fminbnd(@(tn) fit_mat_and_test(IX, IA, IB, N, ids, 3, ...
                                            tn), 0, 5, options);
fprintf(1, 'optimal trace norm: %f\n', trace_norm);
[x S] =  fit_mat(IX, IA, IB, N, ids, iter, trace_norm);


