function plot_feature(img_files, dirname, dataset, ids, name, f, attribute)

%img_base_url = ['http://65.215.1.20/faces/data/' dataset '/'];
img_base_url = ['file:///home/tamuz/dev/simexp/images/' dataset '/'];

small_image_size = 70;

Iwrong = find(f' ~= attribute & attribute > 0);
fprintf('accuracy percentage: %f (%d / %d)\n', 100 - 100 * length(Iwrong) ...
        / length(f), length(f) - length(Iwrong), length(f));

f = f + rand(size(f))*0.5;
%[temp I] = sort(f);
%f(I) = 1:length(f);
f = f - min(f) + 0.01;
f = ceil (f / max(f) * 24);


image_size = 50;

filename = [dirname '/att_' name '.html'];
fprintf('writing to %s\n', filename);
f1 = fopen(filename, 'w');
fprintf(f1, '<html>\n');
fprintf(f1, '<head><title>%s</title></head>\n', name);
fprintf(f1, '<body>\n');
for jj = 1:length(Iwrong)
    j = Iwrong(jj);
    ypos = (1 + attribute(j)) * image_size * 1.05;
    xpos = jj * image_size * 1.05;
    s = '<img name = "img%d" src = "%s%s" style = "position:absolute; left: %d; top:%d;" height = %d width = %d title="%s"/>\n';
    fprintf(f1, s, j, img_base_url, img_files{ids(j) + 1}, floor(xpos), ...
            floor(ypos), image_size, image_size, img_files{ids(j) + ...
                        1});
    %    fprintf('%s %d %f %f\n', img_files{ids(j) + 1}, attribute(j), ...
    %       xpos, ypos);
end

%fprintf(f1, 'plot:\n ');


[temp I] = sort(((f-mean(f)).^2));
I = I(end:-1:1);
%I = length(f):-1:1;
hist_vec = zeros(max(f), 1);
for jj = 1:length(ids)
    j = I(jj);
    %    ypos = jj * (image_size / 2);
    %    xpos = f(j) * 1000;
    
    ypos = (hist_vec(f(j))+4) * image_size * 1.05;
    hist_vec(f(j)) = hist_vec(f(j)) + 1;
    xpos = (f(j) - 1) * image_size * 1.05;
    s = '<img name = "img%d" src = "%s%s" style = "position:absolute; left: %d; top:%d;" height = %d width = %d title="%s"/>\n';
    fprintf(f1, s, j, img_base_url, img_files{ids(j) + 1}, floor(xpos), floor(ypos), image_size, image_size, img_files{ids(j) + 1});
end

fprintf(f1, '</body>\n</html>\n');
fclose(f1);

 