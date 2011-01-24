function [corrects f] = check_features(attributes, names, x, ids, dataset, dirname, feature_num)

img_files = get_image_files(dataset);


%f = fit_feature(x, attributes(:, feature_num));
f = fit_feature_svm(x, attributes(:, feature_num));
plot_feature(img_files, dirname, dataset, ids, names{feature_num}, ...
             f, attributes(:, feature_num));
corrects = length(find(f' == attributes(:, feature_num)));