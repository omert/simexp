function x = create_next_round(datafile , filename, dataset, ids, ...
                               core_size, max_norm)

load(datafile);
[num_obj, d] = size(x);


x = fit_mat(IX, IA, IB, N, ids, 100, max_norm);
save_experiement_data(datafile, IX, IA, IB, N, ids, dataset, x);


T = produce_adaptive(x * x', IX, IA, IB, N, core_size);
IXnew = T(:, 1);
IAnew = T(:, 2);
IBnew = T(:, 3);

IXnew = ids(IXnew(:));
IAnew = ids(IAnew(:));
IBnew = ids(IBnew(:));

%show_triples(IXnew, IAnew, IBnew, dataset);

f = fopen(filename, 'w');
for i = 1:length(IXnew)
    fprintf(f, '%d %d %d\n', IXnew(i), IAnew(i), IBnew(i));
end
fclose(f);
