dataset = 'newtiles';

load(['../turkexps/' dataset '/all.data.mat'])
Sfit = fit_mat_and_trace(IX, IA, IB, N, ids, 20);
xfit = x;
%xfit = fit(rand(size(x)), IX, IA, IB, N, 6);
%save_experiement_data(['../turkexps/' dataset '/small/all.data.mat'], IX, IA, IB, N, ids, dataset, xfit);

fprintf(1, 'optimization fit to sample data: %f\n', model_likelihood(xfit, ...
                                                  IX, IA, IB, N));

load(['../turkexps/' dataset '/heldout.data.mat'])
[L percent_right] = mat_model_likelihood(Sfit, IX, IA, IB, N);
fprintf(1, 'update fit to heldout data: %f percent right: %f\n', L, ...
        percent_right);

fprintf(1, 'optimization fit to heldout data: %f\n', model_likelihood(xfit, ...
                                                  IX, IA, IB, N));
