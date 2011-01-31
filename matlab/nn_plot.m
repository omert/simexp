function nn_plot(x, ids, dataSetName, Iplot, IX, IA, IB, N)

filename = ['../data/' dataSetName '/nn.html'];
img_base_url = ['/home/tamuz/dev/simexp/images/' dataSetName '/'];
img_files = get_image_files(dataSetName);

small_image_size = 70;
page_size = [1500 1000 small_image_size];
large_image_size = 200;

f1 = fopen(filename, 'w');
fprintf(f1, '<html><title>Neighbors %s</title>\n', dataSetName);
fprintf(f1, '<body>\n');

xii = repmat(row_norm(x), 1, length(x)).^2;
D = -sqrt(xii - 2 * x * x' + xii');

%D = confusion_matrix(x * x', IX, IA, IB, N);

if nargin < 4
    Iplot = 1:length(x);
end

for j = 1:length(Iplot)
    jj = Iplot(j);
    [~, I] = sort(-D(jj, :));
    %    I = [j I];
    ypos = j * (small_image_size + 10);
    for i = 1:20
        xpos = i * (small_image_size + 10);
        imsize = small_image_size;
        if i == 1
            s = ['<img name = "img%d" src = "%s%s" style = "border:1px solid black; position:absolute; ' ...
                 'left: %d; top:%d;" height = %d width = ' ...
                 '%d title="%s %f"/>\n'];
        else
            s = ['<img name = "img%d" src = "%s%s" style = "position:absolute; ' ...
                 'left: %d; top:%d;" height = %d width = ' ...
                 '%d title="%s %f"/>\n'];
        end
        %        fprintf(f1, s, i, img_base_url, img_files{ids(I(i)) + 1}, ...
        %        floor(xpos), floor(ypos), ...
        %        imsize, imsize, img_files{ids(I(i)) + 1}, D(j, I(i)));
        fprintf(f1, s, i, img_base_url, img_files{ids(I(i)) + 1}, ...
                floor(xpos), floor(ypos), ...
                imsize, imsize, img_files{ids(I(i)) + 1},jj);
        
    end
end

fprintf(f1, '</body>\n</html>\n');
fclose(f1);
