function classify(dataset, ids, x, att_name)

n = length(ids);

img_path = ['../images/' dataset '/'];
img_files = get_image_files(dataset);

img_data = {};
for i = 1:length(img_files)
    i
    try
        img_data{i} = imread([img_path img_files{i}]);
    catch me
    end
end
figure(1)
handles = show_all_objects(img_data, dataset, 1:n);
        

f0 = -1 * ones(n, 1);
while true
    figure(1);
    [xtemp ytemp button] = ginput(1);
    I = find(handles == get(get(1,'CurrentAxes'),'Children'));
    if ~isempty(I)
        id = I(1);
        if button == 1
            f0(id) = 0;
        elseif button == 3
            f0(id) = 1;
        end
        fprintf('classified %s as %d\n', img_files{id}, f0(id));
    end
    if button == 2
        save_new_attribute(dataset, ids, f0, att_name);
        
        I = find(f0 > -1);
        fprintf('training on a sample of %d\n', length(I));
        svm_res = svmtrain(f0(I), x(I, :), '-t 0');
        f = svmpredict(ones(n, 1), x, svm_res);
        plot_feature(img_files, '../data/', dataset, ids, 'class_result', ...
                     f, f0');
        handles = show_all_objects(img_data, dataset, 1:n, f);
    end
end


