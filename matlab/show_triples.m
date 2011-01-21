function show_triples(IX, IA, IB, dataset)

img_files = get_image_files(dataset);
image_size = 200;
img_base_url = ['http://65.215.1.20/faces/data/' dataset '/'];


f = fopen(['../temp/new_round_' dataset '.html'], 'w');
fprintf(f, '<html>\n<body><\n>');
for j=1:length(IX)
    ypos = (j - 1) * (image_size + 10);
    xpos = 0;
    s = '<img src = "%s%s" style = "position:absolute; left: %d; top:%d;" height = %d width = %d title="%s"/>\n';
    fprintf(f, s, img_base_url, img_files{IX(j) + 1}, floor(xpos), floor(ypos), image_size, image_size, img_files{IX(j) + 1});
    xpos = xpos + image_size + 10;
    s = '<img src = "%s%s" style = "position:absolute; left: %d; top:%d;" height = %d width = %d alt="%s"/>\n';
    fprintf(f, s, img_base_url, img_files{IA(j) + 1}, floor(xpos), floor(ypos), image_size, image_size, img_files{IA(j) + 1});
    xpos = xpos + image_size + 10;
    s = ['<img src = "%s%s" style = "position:absolute; left: %d; ' ...
         'top:%d;" height = %d width = %d alt="%s"/>\n'];
    fprintf(f, s, img_base_url, img_files{IB(j) + 1}, floor(xpos), floor(ypos), image_size, image_size, img_files{IB(j) + 1});
end

fprintf(f, '</body><\n></html>\n');
fclose(f);
