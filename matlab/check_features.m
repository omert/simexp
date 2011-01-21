function check_features(info_file_name, x, ids, dataset, dirname, feature_num)

img_base_url = ['http://65.215.1.20/faces/data/' dataset '/'];

small_image_size = 70;

[attributes names] = read_info(info_file_name);

f = fit_feature(x, attributes(:, feature_num));


[temp I] = sort(f);
f(I) = 1:length(f);
f = f - min(f) + 0.01;
f = ceil (f / max(f) * 24);

img_files = get_image_files(dataset);

f1 = fopen([dirname '/att_' names{feature_num} '.html'], 'w');
fprintf(f1, '<html>\n');
fprintf(f1, '<head><title>%s</title></head>\n', names{feature_num});
fprintf(f1, '<body>\n');

image_size = 50;
[temp I] = sort(((f-mean(f)).^2));
I = I(end:-1:1);
%I = length(f):-1:1;
hist = zeros(max(f), 1);
for jj = 1:length(x)
    j = I(jj);
    %    ypos = jj * (image_size / 2);
    %    xpos = f(j) * 1000;
    
    ypos = hist(f(j)) * image_size * 1.05;
    hist(f(j)) = hist(f(j)) + 1;
    xpos = (f(j) - 1) * image_size * 1.05;
    s = '<img name = "img%d" src = "%s%s" style = "position:absolute; left: %d; top:%d;" height = %d width = %d title="%s"/>\n';
    fprintf(f1, s, j, img_base_url, img_files{ids(j) + 1}, floor(xpos), floor(ypos), image_size, image_size, img_files{ids(j) + 1});
end

fprintf(f1, '</body>\n</html>\n');
fclose(f1);

 