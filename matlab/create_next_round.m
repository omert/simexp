function x = create_next_round(datafile, filename, num_per_obj)
    
    
load(datafile);

%x = fit_mat(IX, IA, IB, N, ids, 100, 10);
x = fit(rand(length(ids), 3), IX, IA, IB, N, 30);
save_experiement_data(datafile, IX, IA, IB, N, ids, dataSetName, x);

%xd2 =  projectPSD_rank(x, 2);
xd2 = x;

T = produce_adaptive(xd2 * xd2', IX, IA, IB, N, num_per_obj);
IXnew = T(:, 1);
IAnew = T(:, 2);
IBnew = T(:, 3);

show_triples(IXnew, IAnew, IBnew, dataSetName, ids, IX, IA, IB, N, xd2)

IXnew = ids(IXnew(:));
IAnew = ids(IAnew(:));
IBnew = ids(IBnew(:));


f = fopen(filename, 'w');
for i = 1:length(IXnew)
    fprintf(f, '%d %d %d\n', IXnew(i), IAnew(i), IBnew(i));
end
fclose(f);
