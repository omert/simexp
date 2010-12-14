function x = create_next_round(datafile , filename, dataset, num_per_obj)

load(datafile);
[num_obj, d] = size(x);

last_fit_val = 1e100;
fit_val = model_likelihood(x, IX, IA, IB, N);
while last_fit_val - fit_val > 5
    last_fit_val = fit_val;
    [x fit_val] = fit(x, IX, IA, IB, N, 3);
end

save_experiement_data(datafile, IX, IA, IB, N, ids, dataset, x);

IXnew = zeros(num_per_obj, num_obj);
IAnew = zeros(size(IXnew));
IBnew = zeros(size(IXnew));
fprintf('calculating %d * %d = %d new comparisons...\n', num_obj, num_per_obj, num_obj * num_per_obj);
for i=1:num_obj
    Iobj = find(IX == i);
    I0 = IA(Iobj);
    J0 = IB(Iobj);
    N0 = N(Iobj);
    IXnew(:, i) = i;
    [IAnew(:, i), IBnew(:, i)] = approx_best_paired_comp(x, I0, J0, N0, ones(1, num_obj) / num_obj, i, num_per_obj);
end
IXnew = ids(IXnew(:));
IAnew = ids(IAnew(:));
IBnew = ids(IBnew(:));

img_files = get_image_files(dataset);
image_size = 200;
img_base_url = ['http://65.215.1.20/faces/data/' dataset '/'];

f = fopen(['c:\sim\new_round_' dataset '.html'], 'w');
fprintf(f, '<html>\n<body><\n>');
for j=1:length(IXnew)
    ypos = (j - 1) * (image_size + 10);
    xpos = 0;
    s = '<img src = "%s%s" style = "position:absolute; left: %d; top:%d;" height = %d width = %d title="%s"/>\n';
    fprintf(f, s, img_base_url, img_files{IXnew(j) + 1}, floor(xpos), floor(ypos), image_size, image_size, img_files{IXnew(j) + 1});
    xpos = xpos + image_size + 10;
    s = '<img src = "%s%s" style = "position:absolute; left: %d; top:%d;" height = %d width = %d alt="%s"/>\n';
    fprintf(f, s, img_base_url, img_files{IAnew(j) + 1}, floor(xpos), floor(ypos), image_size, image_size, img_files{IAnew(j) + 1});
    xpos = xpos + image_size + 10;
    s = '<img src = "%s%s" style = "position:absolute; left: %d; top:%d;" height = %d width = %d alt="%s"/>\n';
    fprintf(f, s, img_base_url, img_files{IBnew(j) + 1}, floor(xpos), floor(ypos), image_size, image_size, img_files{IBnew(j) + 1});
end

fprintf(f, '</body><\n></html>\n');
fclose(f);

f = fopen(filename, 'w');
for i = 1:length(IXnew)
    fprintf(f, '%d %d %d\n', IXnew(i), IAnew(i), IBnew(i));
end
fclose(f);
