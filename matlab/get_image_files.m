function img_files = get_image_files(dataset)

ids_filename = ['http://65.215.1.20/faces/data/' dataset '/ids.txt'];

img_list = urlread(ids_filename);
if (img_list(end) ~= 13)
    img_list(end + 1) = 13;
end
I = find(img_list == 10);
img_list(I) = [];
I = find(img_list == 13);
k = 1;
img_files = cell(length(I), 1);
for i = 1:length(I)
    img_files{i} = img_list(k:(I(i) - 1));
    k = I(i) + 1;
end
