function run_turk(config_file, trips_file, out_file)

fprintf('running turk on %s %s %s\n', config_file, trips_file, out_file);
[status, result] = system(sprintf(['python ../py/runtrips.py %s %s ' ...
'%s'], config_file, trips_file, out_file), '-echo')

%min_sleep = 10;
%fprintf('sleeping for %d minutes\n', min_sleep);
%sleep(min_sleep * 60);