function x = create_next_round(datafile , filename, dataset, ...
                               num_per_obj, ids)

load(datafile);
[num_obj, d] = size(x);

% $$$ last_fit_val = 1e100;
% $$$ fit_val = model_likelihood(x, IX, IA, IB, N);
% $$$ while last_fit_val - fit_val > 5
% $$$     last_fit_val = fit_val;
% $$$     [x fit_val] = fit(x, IX, IA, IB, N, 3);
% $$$ end

%[x fit_val] = fit(x, IX, IA, IB, N, 6);
x = fit_mat_and_trace(IX, IA, IB, N, ids, 10);

save_experiement_data(datafile, IX, IA, IB, N, ids, dataset, x);

model_likelihood(x, IX, IA, IB, N)

IXnew = zeros(num_per_obj, num_obj);
IAnew = zeros(size(IXnew));
IBnew = zeros(size(IXnew));
fprintf('calculating %d * %d = %d new comparisons...\n', num_obj, num_per_obj, num_obj * num_per_obj);
for i=1:num_obj
    fprintf('object %d of %d\n', i, num_obj);
    Iobj = find(IX == i);
    I0 = IA(Iobj);
    J0 = IB(Iobj);
    N0 = N(Iobj);
    IXnew(:, i) = i;
    [IAnew(:, i), IBnew(:, i)] = approx_best_paired_comp(x, I0, J0, N0, ones(1, num_obj) / num_obj, i, num_per_obj);
end
IXnew = ids(IXnew(:));
IAnew = ids(IAnew(:));
IBnew = ids(IBnew(:));

show_triples(IXnew, IAnew, IBnew, dataset);

f = fopen(filename, 'w');
for i = 1:length(IXnew)
    fprintf(f, '%d %d %d\n', IXnew(i), IAnew(i), IBnew(i));
end
fclose(f);
