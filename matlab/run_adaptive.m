function run_adaptive(dir_name, num_rounds, num_per_round)

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
    create_next_round(datafile, filename, num_per_round);
    run_turk([dir_name config_file(1).name], filename, [filename '.out']);
    load(datafile);
    parse_directory(dir_name, dataSetName, x);
end
