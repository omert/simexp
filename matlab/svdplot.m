function svdplot(x, ids, dataSetName)

filename = ['../data/' dataSetName '/svd.html'];
img_base_url = ['/home/tamuz/dev/simexp/images/' dataSetName '/'];
img_files = get_image_files(dataSetName);

small_image_size = 50;
page_size = [840 1050 small_image_size];
large_image_size = 200;

f1 = fopen(filename, 'w');
fprintf(f1, '<html><title>SVD %s</title>\n', dataSetName);
fprintf(f1, '<body>\n');

%while(min(size(x)) < 3)
%    x(:,end + 1) = rand(length(x), 1) / 1000;
%end

x0 = zeros(size(x));
for i=1:min(size(x))
    x0(:, i) = x(:, i) - mean(x(:, i));
end
[U S ~] = svds(x0, 3);


for i = 1:2
    U(:, i) = U(:, i) - min(U(:, i));
    U(:, i) = U(:, i) / max(U(:, i));
end

for i = 1:length(ids)
%  fprintf('%d %s\n', ids(i), img_files{ids(i) + 1});
end
fprintf('found %d images in list\n', length(img_files));

txt_filename = ['../data/' dataSetName '/svd_' dataSetName '.txt'];
ftxt = fopen(txt_filename, 'w');
for i = 1:length(U)
    
%    aspect = 2;
%    zpos = aspect + U(i, 3);
%    xpos = page_size(1) * ((U(i, 1) - 0.5) / zpos * aspect * 2 + 0.5) ;
%    ypos = page_size(2) * ((U(i, 2) - 0.5) / zpos * aspect * 2 + 0.5);
    xpos = page_size(1) * U(i, 1);
    ypos = page_size(2) * U(i, 2);
    zpos = 1;
    
    fprintf(ftxt, '%s %d %d\n', img_files{ids(i) + 1}, round(xpos), round(ypos));
    
%    z_image_size = small_image_size *(aspect + 0.5 - U(i, 3));
    z_image_size = small_image_size;
    s = '<span onmouseover = "document.img%d.width = %d; document.img%d.height = %d;" onmouseout = "document.img%d.width = %d; document.img%d.height = %d">\n';
    fprintf(f1, s, i, large_image_size, i, large_image_size, i, z_image_size, i, z_image_size);
    s = ['<img name = "img%d" src = "%s%s" style = "position:absolute; ' ...
         'left: %d; top:%d; z-index = %d;border-right:1px solid black;border-bottom:1px solid black" height = %d width = %d title="%s"/>\n'];
    fprintf(f1, s, i, img_base_url, img_files{ids(i) + 1}, floor(xpos), floor(ypos), floor(1000 - 100 * zpos), z_image_size, z_image_size, img_files{ids(i) + 1});
    fprintf(f1, '</span>\n');
%    s = '<span><img src = "%s%s" style = "position:absolute; left: %d; top:%d;"/></span>\n';
%    fprintf(f1, s, img_base_url, img_files{ids(i) + 1}, U(i, 1), U(i, 2));
%    fprintf(f1, '</a>\n');

end
fclose(ftxt);

fprintf(f1, '</body>\n</html>\n');
fclose(f1);

