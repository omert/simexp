function run_adaptive(dir_name, dataset, num_rounds, num_per_round)

config_file = dir([dir_name '*.config']);
if length(config_file) ~= 1
    fprintf('found zero %d config files, there should be just one', length(config_file));
    return;
end

datafile = [dir_name 'all.data.mat'];

for i = 1:num_rounds
    load(datafile);
    fprintf('found data for %d comparisons\n', length(IX));
    filename = [dir_name 'adaptive' sprintf('%8.0f',mod(now*1000000, 100000000)) '.trips'];
    create_next_round(datafile , filename, dataset, num_per_round, ids);
    run_turk([dir_name config_file(1).name], filename, [filename '.out']);
    parse_directory(dir_name, dataset, x);
end
x = fit_mat(IX, IA, IB, N, ids, 100, 7, x * x');
save_experiement_data([dir_name 'all.data.mat'], IX, IA, IB, N, ids, dataset, x);