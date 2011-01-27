function [IX, IA, IB, N, ids] = parse_directory(dir_name, dataset, ...
                                                x, ids_force)

IX = [];
IA = [];
IB = [];
N = [];
ids = [];

files = dir([dir_name '/*.out']) ;
    

for i = 1:length(files)
    fprintf('parsing file %s\n', files(i).name);
    [IX0, IA0, IB0, N0, ids0] = parse_output([dir_name files(i).name], dataset);
    IX = [IX; IX0];
    IA = [IA; IA0];
    IB = [IB; IB0];
    N = [N; N0];
    ids = unique([ids; ids0]);
end
fprintf('found a total of %d triplets\n', length(IX));
if nargin > 3
    ids = ids_force(:);
end
if length(x) == 1
    x = rand(length(ids), x);
end
save_experiement_data([dir_name 'all.data.mat'], IX, IA, IB, N, ids, dataset, x);
