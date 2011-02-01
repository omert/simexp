function rand_vs_adapt(dir_base, dir1, name1, dir2, name2, control_dir, ...
                       bank_dir, dataSetName)

dir1 = [dir_base dir1];
dir2 = [dir_base dir2];
control_dir = [dir_base control_dir];
bank_dir = [dir_base bank_dir];

parse_directory(dir1, dataSetName, 1);
parse_directory(dir2, dataSetName, 1);
parse_directory(control_dir, dataSetName, 1);
parse_directory(bank_dir, dataSetName, 1);

load([control_dir 'all.data.mat']);
IXcontrol = IX;
IAcontrol = IA;
IBcontrol = IB;
Ncontrol = N;

load([bank_dir 'all.data.mat']);
IXbank = IX;
IAbank = IA;
IBbank = IB;
Nbank = N;

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
num_points = 27;
sample_sizes = floor(linspace(9.5 * length(ids), maxn, num_points))

x1 = {};
x2 = {};
S1 = zeros(length(ids), length(ids));
S2 = S1;
num_queries = 20;

for i = 1:length(sample_sizes)
    m = sample_sizes(i);
    %    x1{i} = fit_mat(IX1(1:m), IA1(1:m), IB1(1:m), N1(1:m), ids, 100, ...
    %                10, S1);
    %x2{i} = fit_mat(IX2(1:m), IA2(1:m), IB2(1:m), N2(1:m), ids, 100, ...
    %                10, S2);
    x1{i} = fit(rand(length(ids), 3), IX1(1:m), IA1(1:m), IB1(1:m), ...
                N1(1:m), 30);
    x2{i} = fit(rand(length(ids), 3), IX2(1:m), IA2(1:m), IB2(1:m), ...
                N2(1:m), 30);
    S1 = x1{i}*x1{i}';
    S2 = x2{i}*x2{i}';
    [ll1(i) corrects1(i) ] = mat_model_likelihood(S1, IXcontrol, IAcontrol, IBcontrol, ...
                                  Ncontrol);
    [ll2(i) corrects2(i) ] = mat_model_likelihood(S2, IXcontrol, IAcontrol, IBcontrol, ...
                                  Ncontrol);
    igain1(i, :) = information_gain(S1, IXcontrol, IAcontrol, ...
                                    IBcontrol, Ncontrol)';
    igain2(i, :) = information_gain(S2, IXcontrol, IAcontrol, ...
                                    IBcontrol, Ncontrol)';
    temp1 = predict_using_bank(S1, IXbank, IAbank, IBbank, Nbank, num_queries);
    metrics1(i, :) = temp1(:, end)';
    temp2 = predict_using_bank(S2, IXbank, IAbank, IBbank, Nbank, num_queries);
    metrics2(i, :) = temp2(:, end)';
    save(['model_comparison_' dataSetName]);
end



