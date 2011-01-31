function compare_to_bank(dataSetName)

load(['model_comparison_' dataSetName]);

parse_directory(dir1, dataSetName, 1);
parse_directory(dir2, dataSetName, 1);
parse_directory(bank_dir, dataSetName, 1);


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
num_points = 20;
sample_sizes = round((1:num_points) * maxn / num_points);
S1 = zeros(length(ids), length(ids));
S2 = S1;
num_queries = 20;

for i = 1:num_points
    m = sample_sizes(i);
    S1 = x1{i}*x1{i}';
    S2 = x2{i}*x2{i}';
    temp1 = predict_using_bank(S1, IXbank, IAbank, IBbank, Nbank, num_queries);
    metrics1(i, :) = temp1(:, end)';
    temp2 = predict_using_bank(S2, IXbank, IAbank, IBbank, Nbank, num_queries);
    metrics2(i, :) = temp2(:, end)';
    save(['model_comparison_' dataSetName]);
end



