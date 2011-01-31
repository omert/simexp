function show_triples(iTX, iTA, iTB, dataSetName, ids, IX, IA, IB, N, x)

img_files = get_image_files(dataSetName);
image_size = 200;
small_image_size = round(image_size / 3 * 2);
img_base_url = ['file:///home/tamuz/dev/simexp/images/' dataSetName '/'];

if nargin >= 10
    P = confusion_matrix(x * x', IX, IA, IB, N);
    
    P = P .* (1 - eye(length(P)));
    P = normalize_dist(P, 2);
    
    P1 = ones(length(iTX), length(x));
    P2 = ones(length(iTX), length(x));
    probs = paired_comp_prob(x, x, iTA, iTB);
    for i = 1:length(iTX)
        P1(i, :) = P(iTX(i), :) .* probs(i, :);
        P2(i, :) = P(iTX(i), :) .* (1 - probs(i, :));
    end
    P1 = normalize_dist(P1, 2);
    P2 = normalize_dist(P2, 2);
end


f = fopen(['../data/' dataSetName '/new_adaptive_round.html'], 'w');
fprintf(f, '<html><title>New Round %s</title>\n', dataSetName);
fprintf(f, '<table border="2" style="border-collapse: collapse;" ><tbody>\n');
for j=1:length(iTX)
    fprintf(f, '<tr>\n');
    fprintf(f, '<td>\n');
    s = ['<img src = "%s%s" height = %d width = %d title="%s"/>\n'];
    fprintf(f, s, img_base_url, img_files{ids(iTX(j)) + 1},  ...
            image_size, image_size, img_files{ids(iTX(j)) + 1});
    fprintf(f, '</td>\n');
    
    fprintf(f, '<td>\n');
    fprintf(f, '<table><tbody>\n');
    fprintf(f, '<tr border = "1">\n');
    fprintf(f, '<td>\n');
    s = ['<img src = "%s%s" height = %d width = %d title="%s"/>\n'];
    fprintf(f, s, img_base_url, img_files{ids(iTA(j)) + 1},  ...
            image_size, image_size, img_files{ids(iTA(j)) + 1});
    fprintf(f, '</td>\n');
    fprintf(f, '</tr>\n');
    
    fprintf(f, '<tr>\n');
    fprintf(f, '<td>\n');
    s = ['<img src = "%s%s" height = %d width = %d title="%s"/>\n'];
    fprintf(f, s, img_base_url, img_files{ids(iTB(j)) + 1},  ...
            image_size, image_size, img_files{ids(iTB(j)) + 1});
    fprintf(f, '</td>\n');
    fprintf(f, '</tr>\n');
    fprintf(f, '</tbody></table>\n');
    fprintf(f, '</td>\n');

    
    if nargin >= 10

        fprintf(f, '<td>\n');
        fprintf(f, '<table><tbody>\n');
        
        [~, I] = sort(-P1(j, :));
        fprintf(f, '<tr border = "1">\n');
        for i = 1:10
            fprintf(f, '<td>\n');
            s = ['<img src = "%s%s" height = %d width = %d title="%f"/>\n'];
            fprintf(f, s, img_base_url, img_files{ids(I(i)) + 1},  ...
                    small_image_size, small_image_size, P1(j, I(i)));
            fprintf(f, '</td>\n');
        end
        fprintf(f, '</tr>\n');

        [~, I] = sort(-P2(j, :));
        fprintf(f, '<tr border = "1">\n');
        for i = 1:10
            fprintf(f, '<td>\n');
            s = ['<img src = "%s%s" height = %d width = %d title="%f"/>\n'];
            fprintf(f, s, img_base_url, img_files{ids(I(i)) + 1},  ...
                    small_image_size, small_image_size, P2(j, I(i)));
            fprintf(f, '</td>\n');
        end
        fprintf(f, '</tr>\n');

        
        [~, I] = sort(-P(iTX(j), :));
        fprintf(f, '<tr border = "1">\n');
        for i = 1:10
            fprintf(f, '<td>\n');
            s = ['<img src = "%s%s" height = %d width = %d title="%f"/>\n'];
            fprintf(f, s, img_base_url, img_files{ids(I(i)) + 1},  ...
                    small_image_size, small_image_size, P(iTX(j), I(i)));
            fprintf(f, '</td>\n');
        end
        fprintf(f, '</tr>\n');

        fprintf(f, '</tbody></table>\n');
        fprintf(f, '</td>\n');
    end
    
    
    fprintf(f, '</tr>\n');
end
fprintf(f, '</tbody></table>\n');
fprintf(f, '</body><\n></html>\n');
fclose(f);
