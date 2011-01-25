function show_triples(idsX, idsA, idsB, dataset)

img_files = get_image_files(dataset);
image_size = 200;
img_base_url = ['file:///home/tamuz/dev/simexp/images/' dataset '/'];


f = fopen(['../data/' dataset '/new_adaptive_round.html'], 'w');
fprintf(f, '<html>\n<body><\n>');
for j=1:length(idsX)
    ypos = (j - 1) * (image_size + 10);
    xpos = 0;
    s = ['<img src = "%s%s" style = "position:absolute; left: %d; ' ...
         'top:%d;" height = %d width = %d title="%s"/>\n'];
    fprintf(f, s, img_base_url, img_files{idsX(j) + 1}, floor(xpos), ...
            floor(ypos), image_size, image_size, img_files{idsX(j) + 1});
    xpos = xpos + image_size + 10;
    s = ['<img src = "%s%s" style = "position:absolute; left: %d; ' ...
         'top:%d;" height = %d width = %d title="%s"/>\n'];
    fprintf(f, s, img_base_url, img_files{idsA(j) + 1}, floor(xpos), ...
            floor(ypos), image_size, image_size, img_files{idsA(j) + 1});
    xpos = xpos + image_size + 10;
    s = ['<img src = "%s%s" style = "position:absolute; left: %d; ' ...
         'top:%d;" height = %d width = %d title="%s"/>\n'];
    fprintf(f, s, img_base_url, img_files{idsB(j) + 1}, floor(xpos), ...
            floor(ypos), image_size, image_size, img_files{idsB(j) + 1});
end

fprintf(f, '</body><\n></html>\n');
fclose(f);
