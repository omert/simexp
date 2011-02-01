function create_exhaustive_tripels(ids, sample_ids, filename)


f = fopen(filename, 'w');
for i = 1:length(sample_ids)
    x = sample_ids(i);
    for j = 1:length(ids)
        a = ids(j);
        for k = 1:length(ids)
            b = ids(k);
            if x ~= a && x ~= b && a ~= b
                fprintf(f, '%d %d %d\n', x, a, b);
            end
        end
    end
end
fclose(f);
type(filename);


