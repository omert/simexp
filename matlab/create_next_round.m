function x = create_next_round(datafile , filename, dataset, ...
                               num_per_obj, ids)

load(datafile);
[num_obj, d] = size(x);


%[x fit_val] = fit(x, IX, IA, IB, N, 6);
%x = fit_mat(IX, IA, IB, N, ids, 5, 1, x * x');
%save_experiement_data(datafile, IX, IA, IB, N, ids, dataset, x);

model_likelihood(x, IX, IA, IB, N)

if 0
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
        fprintf('%f\n', paired_comp_prob(x(i, :), x, IAnew(1, i), IBnew(1, ...
                                                          i)));
    end
else
    T = produce_adaptive(x * x', IX, IA, IB, N);
    IXnew = T(:, 1);
    IAnew = T(:, 2);
    IBnew = T(:, 3);
    keyboard
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
