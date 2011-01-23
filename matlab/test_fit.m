load(['../turkexps/neckties/small/all.data.mat'])
[xfit Sfit] = fit_mat(IX, IA, IB, N, ids, 20, 0.2);

load(['../turkexps/neckties/small/control/all.data.mat'])
[L percent_right] = mat_model_likelihood(Sfit, IX, IA, IB, N);
fprintf(1, 'update fit to heldout data: %f percent right: %f\n', L, ...
        percent_right);

