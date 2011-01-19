load('../turkexps/newtiles/all.data.mat')
Sfit = fit_mat(IX, IA, IB, N, ids);
xfit = fit(rand(size(x)), IX, IA, IB, N, 6);
save_experiement_data('../turkexps/newtiles/all.data.mat', IX, IA, IB, N, ids, dataset, xfit);
load('../turkexps/newtiles/heldout.data.mat')
fprintf(1, 'update fit to heldout data: %f\n', mat_model_likelihood(Sfit, ...
                                                  IX, IA, IB, N));
fprintf(1, 'optimization fit to heldout data: %f\n', model_likelihood(xfit, ...
                                                  IX, IA, IB, N));
