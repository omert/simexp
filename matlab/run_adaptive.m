function run_adaptive(dir_name, dataset, num_rounds, num_per_round)

config_file = dir([dir_name '*.config']);
if length(config_file) ~= 1
    fprintf('found zero %d config files, there should be just one', length(config_file));
    return;
end


for i = 1:num_rounds
    datafile = [dir_name 'all.data.mat'];
    load(datafile);
    fprintf('found data for %d comparisons\n', length(IX));
    filename = [dir_name 'adaptive' sprintf('%d',floor(rand*100000)) '.trips'];
    create_next_round(datafile , filename, dataset, num_per_round);
    run_turk([dir_name config_file(1).name], filename, [filename '.out']);
    parse_directory(dir_name, dataset, x);
end
x=fit(x, IX, IA, IB, N, 200);
save_experiement_data([dir_name 'all.data.mat'], IX, IA, IB, N, ids, dataset, x);