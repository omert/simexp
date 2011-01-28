function show_triples(idsX, idsA, idsB, dataset, ids, IX, IA, IB, N, x)

img_files = get_image_files(dataset);
image_size = 200;
small_image_size = round(image_size / 3 * 2);
img_base_url = ['file:///home/tamuz/dev/simexp/images/' dataset '/'];

if nargin >= 10
    P = confusion_matrix(x * x', IX, IA, IB, N);
    
    P = P .* (1 - eye(length(P)));
    P = normalize_dist(P, 2);
    
    P1 = ones(length(idsX), length(x));
    P2 = ones(length(idsX), length(x));
    probs = paired_comp_prob(x, x, idsA + 1, idsB + 1);
    for i = 1:length(idsX)
        iX = idsX(i) + 1;
        P1(i, :) = P(iX, :) .* probs(i, :);
        P2(i, :) = P(iX, :) .* (1 - probs(i, :));
    end
    P1 = normalize_dist(P1, 2);
    P2 = normalize_dist(P2, 2);
end


f = fopen(['../data/' dataset '/new_adaptive_round.html'], 'w');
fprintf(f, '<html>\n<body>\n');
fprintf(f, '<table border="2" style="border-collapse: collapse;" ><tbody>\n');
for j=1:length(idsX)
    fprintf(f, '<tr>\n');
    fprintf(f, '<td>\n');
    s = ['<img src = "%s%s" height = %d width = %d title="%s"/>\n'];
    fprintf(f, s, img_base_url, img_files{idsX(j) + 1},  ...
            image_size, image_size, img_files{idsX(j) + 1});
    fprintf(f, '</td>\n');
    
    fprintf(f, '<td>\n');
    fprintf(f, '<table><tbody>\n');
    fprintf(f, '<tr border = "1">\n');
    fprintf(f, '<td>\n');
    s = ['<img src = "%s%s" height = %d width = %d title="%s"/>\n'];
    fprintf(f, s, img_base_url, img_files{idsA(j) + 1},  ...
            image_size, image_size, img_files{idsA(j) + 1});
    fprintf(f, '</td>\n');
    fprintf(f, '</tr>\n');
    
    fprintf(f, '<tr>\n');
    fprintf(f, '<td>\n');
    s = ['<img src = "%s%s" height = %d width = %d title="%s"/>\n'];
    fprintf(f, s, img_base_url, img_files{idsB(j) + 1},  ...
            image_size, image_size, img_files{idsB(j) + 1});
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

        
        [~, I] = sort(-P(idsX(j) + 1, :));
        fprintf(f, '<tr border = "1">\n');
        for i = 1:10
            fprintf(f, '<td>\n');
            s = ['<img src = "%s%s" height = %d width = %d title="%f"/>\n'];
            fprintf(f, s, img_base_url, img_files{ids(I(i)) + 1},  ...
                    small_image_size, small_image_size, P(j, I(i)));
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
