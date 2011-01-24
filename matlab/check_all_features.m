function check_all_features(x, ids, dataset)

    dirname = ['../data/' dataset '/'];
    info_file_name = [dirname 'info.csv'];
                     
[attributes names] = read_info(info_file_name, ids);


filename = [dirname '/index.html'];
fprintf('writing to %s\n', filename);
f1 = fopen(filename, 'w');
fprintf(f1, '<html>\n');
fprintf(f1, '<head><title></title></head>\n');
fprintf(f1, '<body>\n');

n = length(x);
for i=1:length(names)
    c = check_features(attributes, names, x, ids, dataset, dirname, i);
    fprintf(f1, ['<a href="att_' names{i} '.html">' names{i} '</a>']);
    fprintf(f1, '____ %d out of %d (%.1f percent)</a></br>\n', c, ...
            n, 100 * c / n); 
end


fprintf(f1, '</body>\n</html>\n');
fclose(f1);


