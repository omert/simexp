function check_features(info_file_name, x, ids, dataset, filename)

img_base_url = ['http://65.215.1.20/faces/data/' dataset '/'];

small_image_size = 70;

[attributes names] = read_info(info_file_name);

att = 3;

f = fit_feature(x, attributes(:, att));


f = f - min(f);
f = f / max(f);

img_files = get_image_files(dataset);

f1 = fopen(filename, 'w');
fprintf(f1, '<html>\n');
fprintf(f1, '<body>\n');
fprintf(f1, '<h1>%s</h1>\n', names{att});

image_size = 100;
for j = 1:length(x)
    ypos = j * (image_size + 10);
    xpos = f(j) * 800;
    s = '<img name = "img%d" src = "%s%s" style = "position:absolute; left: %d; top:%d;" height = %d width = %d title="%s"/>\n';
    fprintf(f1, s, j, img_base_url, img_files{ids(j) + 1}, floor(xpos), floor(ypos), image_size, image_size, img_files{ids(j) + 1});
end

fprintf(f1, '</body>\n</html>\n');
fclose(f1);

 