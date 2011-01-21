function L = fit_mat_and_test(IX, IA, IB, N, ids, iter, S, trace_norm)

m = length(IX);
I = randperm(m);
Isample = I(1:(floor(m / 2)));
Icontrol = I((floor(m / 2)+1):end);

S = fit_mat(IX(Isample), IA(Isample), IB(Isample), N(Isample), ids, ...
            iter, S, trace_norm);
L = mat_model_likelihood(S, IX(Icontrol), IA(Icontrol), IB(Icontrol), ...
                         N(Icontrol));
fprintf(1, 'trace norm: %f    fit to control: %f\n', trace_norm, L);
