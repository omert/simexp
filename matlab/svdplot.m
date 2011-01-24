function svdplot(x, ids, dataset, filename, IX, IA, IB, N)

img_base_url = ['/home/tamuz/dev/simexp/images/' dataset '/'];

small_image_size = 70;
page_size = [1500 1000 small_image_size];
large_image_size = 200;

f1 = fopen(filename, 'w');
fprintf(f1, '<html>\n');
fprintf(f1, '<body>\n');

%while(min(size(x)) < 3)
%    x(:,end + 1) = rand(length(x), 1) / 1000;
%end

x0 = zeros(size(x));
for i=1:min(size(x))
    x0(:, i) = x(:, i) - mean(x(:, i));
end
[U S ~] = svds(x0, 3);

img_files = get_image_files(dataset);

for i = 1:2
    U(:, i) = U(:, i) - min(U(:, i));
    U(:, i) = U(:, i) / max(U(:, i));
end

for i = 1:length(ids)
%  fprintf('%d %s\n', ids(i), img_files{ids(i) + 1});
end
fprintf('found %d images in list\n', length(img_files));

for i = 1:length(U)
%    aspect = 2;
%    zpos = aspect + U(i, 3);
%    xpos = page_size(1) * ((U(i, 1) - 0.5) / zpos * aspect * 2 + 0.5) ;
%    ypos = page_size(2) * ((U(i, 2) - 0.5) / zpos * aspect * 2 + 0.5);
    xpos = page_size(1) * U(i, 1);
    ypos = page_size(2) * U(i, 2);
    zpos = 1;

%    z_image_size = small_image_size *(aspect + 0.5 - U(i, 3));
    z_image_size = small_image_size;
    s = '<span onmouseover = "document.img%d.width = %d; document.img%d.height = %d;" onmouseout = "document.img%d.width = %d; document.img%d.height = %d">\n';
    fprintf(f1, s, i, large_image_size, i, large_image_size, i, z_image_size, i, z_image_size);
    s = '<img name = "img%d" src = "%s%s" style = "position:absolute; left: %d; top:%d; z-index = %d;" height = %d width = %d title="%s"/>\n';
    fprintf(f1, s, i, img_base_url, img_files{ids(i) + 1}, floor(xpos), floor(ypos), floor(1000 - 100 * zpos), z_image_size, z_image_size, img_files{ids(i) + 1});
    fprintf(f1, '</span>\n');
%    s = '<span><img src = "%s%s" style = "position:absolute; left: %d; top:%d;"/></span>\n';
%    fprintf(f1, s, img_base_url, img_files{ids(i) + 1}, U(i, 1), U(i, 2));
%    fprintf(f1, '</a>\n');
end

xii = repmat(row_norm(x), 1, length(x)).^2;
D = sqrt(xii - 2 * x * x' + xii');

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

