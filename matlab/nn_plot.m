function nn_plot(x, ids, dataset, IX, IA, IB, N)

filename = ['../data/' dataset '/nn.html'];
img_base_url = ['/home/tamuz/dev/simexp/images/' dataset '/'];

small_image_size = 70;
page_size = [1500 1000 small_image_size];
large_image_size = 200;

f1 = fopen(filename, 'w');
fprintf(f1, '<html>\n');
fprintf(f1, '<body>\n');

%xii = repmat(row_norm(x), 1, length(x)).^2;
%D = sqrt(xii - 2 * x * x' + xii');

D = confusion_matrix(x * x', IX, IA, IB, N);
for j = 1:length(x)
    [~, I] = sort(-D(j, :));
    I = [j I];
    ypos = j * (small_image_size + 10) + page_size(2);
    for i = 1:20
        xpos = i * (small_image_size + 10);
        if 1
            imsize = small_image_size;
        else
            imsize = floor(small_image_size * sqrt(D(j, I(i)) / D(j, ...
                                                             I(2))));
        end
        s = ['<img name = "img%d" src = "%s%s" style = "position:absolute; ' ...
             'left: %d; top:%d; z-index = %d;" height = %d width = ' ...
        '%d title="%s %f"/>\n'];
        fprintf(f1, s, i, img_base_url, img_files{ids(I(i)) + 1}, ...
                floor(xpos), floor(ypos), floor(1000 - 100 * zpos), ...
                imsize, imsize, img_files{ids(I(i)) + 1}, D(j, I(i)));
        
    end
end

fprintf(f1, '</body>\n</html>\n');
fclose(f1);
