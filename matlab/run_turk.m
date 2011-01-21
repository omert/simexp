function run_turk(config_file, trips_file, out_file)

fprintf('running turk on %s %s %s\n', config_file, trips_file, out_file);
[status, result] = system(sprintf('../py/runtrips.py %s %s %s', config_file, trips_file, out_file), '-echo')