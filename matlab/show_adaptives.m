function show_adaptives(dataSetName, dir_name, plotIds, adapt)

img_base_url = ['/home/tamuz/dev/simexp/images/' dataSetName '/'];
img_files = get_image_files(dataSetName);
image_size = 200;
small_image_size = round(image_size / 2);

if adapt
    files = dir([dir_name '/adaptive*.out']);
else
    files = dir([dir_name '/*.out']);
end

T = {};
A = {};
for j = 1:length(plotIds)
    A{j} = [];
end

for i = 1:length(files)
    fprintf('reading %s\n', [dir_name files(i).name]);
    T = load([dir_name files(i).name]);
    for j = 1:length(plotIds)
        jj = plotIds(j);
        if ~isempty(T);
            I = find(T(:, 1) == jj);
            fprintf('    found %d for %d\n', length(I), jj);
            A{j} = [A{j}; T(I, [2 3])];
        end
    end
end
if adapt
    f = fopen(['../data/' dataSetName '/adaptive_trajectory.html'], ...
              'w');
else
    f = fopen(['../data/' dataSetName '/trajectory.html'], ...
              'w');
end
fprintf(f, '<html><title>Trajectory %s</title>\n', dataSetName);
fprintf(f, '<table border="2" style="border-collapse: collapse;" ><tbody>\n');
fprintf(f, '<tr>\n');
for j=1:length(plotIds)
    if isempty(A{j})
        fprintf('got nothing for %d\n', plotIds(j));
        continue;
    end

    jj = plotIds(j);
    fprintf(f, '<td>\n');
    s = ['<img src = "%s%s" height = %d width = %d title="%d" style ' ...
         '= "border:0px solid black; margin:20px"/>\n'];
    fprintf(f, s, img_base_url, img_files{jj + 1},  ...
            image_size, image_size, jj);
    fprintf(f, '</td>\n');
end
fprintf(f, '</tr>\n');


fprintf(f, '<tr>\n');
for j=1:length(plotIds)

    if isempty(A{j})
        continue;
    end

    fprintf(f, '<td  valign="top">\n');
    fprintf(f, '<table><tbody>\n');

    for i = 1:length(A{j})
        fprintf(f, '<tr>\n');

        
        if rand > 0.5
            a = A{j}(i, 1);
            b = A{j}(i, 2);
            bordera = 'style="border:5px solid red; padding:7px"';
            borderb = '';
        else
            b = A{j}(i, 1);
            a = A{j}(i, 2);
            borderb = 'style="border:5px solid red; padding:7px"';
            bordera = '';
        end
        if 1==1
            fprintf(f, '<td>\n');
            s = ['<img src = "%s%s" height = %d width = %d %s/>\n'];
            fprintf(f, s, img_base_url, img_files{a + 1},  ...
                    small_image_size, small_image_size, bordera);
            fprintf(f, '</td>\n');
            
            fprintf(f, '<td>\n');
            s = ['<img src = "%s%s" height = %d width = %d %s/>\n'];
            fprintf(f, s, img_base_url, img_files{b + 1},  ...
                    small_image_size, small_image_size, borderb);
            fprintf(f, '</td>\n');
        else
            fprintf(f, '<td>\n');
            s = ['<img src = "%s%s" height = %d width = %d/>\n'];
            fprintf(f, s, img_base_url, img_files{A{j}(i, 1) + 1},  ...
                    small_image_size, small_image_size);
            fprintf(f, '</td>\n');
            
            fprintf(f, '<td>\n');
            s = ['<img src = "%s%s" height = %d width = %d/>\n'];
            fprintf(f, s, img_base_url, img_files{A{j}(i, 2) + 1},  ...
                    small_image_size, small_image_size);
            fprintf(f, '</td>\n');
        end
        
        fprintf(f, '</tr>\n');
                
    end
    

        
    
    fprintf(f, '</tbody></table>\n');
    fprintf(f, '</td>\n');
end
fprintf(f, '</tr>\n');


fprintf(f, '</tbody></table>\n');
fprintf(f, '</body></html>\n');
fclose(f);

