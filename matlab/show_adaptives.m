function show_adaptives(dataSetName, dir_name, plotIds)

img_base_url = ['/home/tamuz/dev/simexp/images/' dataSetName '/'];
img_files = get_image_files(dataSetName);
image_size = 200;
small_image_size = round(image_size / 2);

files = dir([dir_name '/adaptive*.out']);

T = {};
A = {};
for j = 1:length(plotIds)
    A{j} = [];
end

for i = 1:length(files)
    T = load([dir_name files(i).name]);
    for j = 1:length(plotIds)
        jj = plotIds(j);
        if ~isempty(T);
            I = find(T(:, 1) == jj);
            A{j} = [A{j}; T(I, [2 3])];
        end
    end
end

f = fopen(['../data/' dataSetName '/adaptive_trajectory.html'], 'w');
fprintf(f, '<html>\n<body>\n');
fprintf(f, '<table border="2" style="border-collapse: collapse;" ><tbody>\n');
for j=1:length(plotIds)
    jj = plotIds(j);
    fprintf(f, '<tr>\n');
    fprintf(f, '<td>\n');
    s = ['<img src = "%s%s" height = %d width = %d title="%d"/>\n'];
    fprintf(f, s, img_base_url, img_files{jj + 1},  ...
            image_size, image_size, jj);
    fprintf(f, '</td>\n');
    

    
    fprintf(f, '<td>\n');
    fprintf(f, '<table><tbody>\n');
    
    fprintf(f, '<tr border = "1">\n');
    for i = 1:length(A{j})
        fprintf(f, '<td>\n');
        s = ['<img src = "%s%s" height = %d width = %d/>\n'];
        fprintf(f, s, img_base_url, img_files{A{j}(i, 1) + 1},  ...
                small_image_size, small_image_size);
        fprintf(f, '</td>\n');
    end
    fprintf(f, '</tr>\n');
    fprintf(f, '<tr border = "1">\n');
    for i = 1:length(A{j})
        fprintf(f, '<td>\n');
        s = ['<img src = "%s%s" height = %d width = %d/>\n'];
        fprintf(f, s, img_base_url, img_files{A{j}(i, 2) + 1},  ...
                small_image_size, small_image_size);
        fprintf(f, '</td>\n');
    end
    fprintf(f, '</tr>\n');
    

        
    
    fprintf(f, '</tbody></table>\n');
    fprintf(f, '</td>\n');
    fprintf(f, '</tr>\n');
end
fprintf(f, '</tbody></table>\n');
fprintf(f, '</body></html>\n');
fclose(f);

