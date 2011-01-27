function rand_vs_adapt(dir1, name1, dir2, name2, control_dir, dataset)

parse_directory(dir1, dataset, 1);
parse_directory(dir2, dataset, 1);
parse_directory(control_dir, dataset, 1);

load([control_dir 'all.data.mat']);
IXcontrol = IX;
IAcontrol = IA;
IBcontrol = IB;
Ncontrol = N;

load([dir1 'all.data.mat']);
IX1 = IX;
IA1 = IA;
IB1 = IB;
N1 = N;

load([dir2 'all.data.mat']);
IX2 = IX;
IA2 = IA;
IB2 = IB;
N2 = N;

maxn = min(length(IX1), length(IX2));
num_points = 10;
sample_sizes = round((1:num_points) * maxn / num_points);
for i = 1:num_points
    m = sample_sizes(i);
    x1 = fit_mat(IX1(1:m), IA1(1:m), IB1(1:m), N1(1:m), ids, 100, 4);
    x2 = fit_mat(IX2(1:m), IA2(1:m), IB2(1:m), N2(1:m), ids, 100, 4);
    ll1(i) = mat_model_likelihood(x1 * x1', IXcontrol, IAcontrol, ...
                                  IBcontrol, Ncontrol);
    ll2(i) = mat_model_likelihood(x2 * x2', IXcontrol, IAcontrol, ...
                                  IBcontrol, Ncontrol);
    igain1(i, :) = information_gain(x1 * x1', IXcontrol, IAcontrol, ...
                                  IBcontrol, Ncontrol)';
    igain2(i, :) = information_gain(x2 * x2', IXcontrol, IAcontrol, ...
                                  IBcontrol, Ncontrol)';
    save(['model_comparison_' dataset]);
end



