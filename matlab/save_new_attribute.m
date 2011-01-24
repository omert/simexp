function save_new_attribute(dataset, ids, att, att_name)

img_files = get_image_files(dataset);
infofile = ['../data/' dataset '/info.csv'];
[attributes names] = read_info(infofile, ids);
f = fopen(infofile, 'w');
fprintf(f, 'id,image,att_%s', att_name);
for i = 1:length(names)
    if ~strcmp(names{i}, att_name)
        fprintf(f, ',att_%s', names{i});
    end
end
fprintf(f, '\n');

for i = 1:length(ids)
    fprintf(f,'%d,%s,%d', ids(i), img_files{i}, att(i) == 1);
    for j = 1:length(names)
        if ~strcmp(names{j}, att_name)
            fprintf(f, ',%d', attributes(i, j));
        end
    end
    fprintf(f, '\n');
end



