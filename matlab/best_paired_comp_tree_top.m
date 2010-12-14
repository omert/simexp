function [ibest, jbest, pbest, kldiv, tree_image] = best_paired_comp_tree_top(x, I0, J0, N0, prior0, exclusions, manual, depth, img_files_path, img_files, ids)

[ibest, jbest, pbest, kldiv] = best_paired_comp(x, I0, J0, N0, prior0, exclusions, manual);
image_left = imread([img_files_path img_files{ids(ibest) + 1}]);
image_right = imread([img_files_path img_files{ids(jbest) + 1}]);

image_left = imresize(image_left, 2^(-depth));
image_right = imresize(image_right, 2^(-depth));

if depth < 2

    N0(length(N0) + 1, 1) = 1;
    prior0(ibest) = 1e-100;
    prior0(jbest) = 1e-100;
    prior0 = prior0 / sum(prior0);
    depth = depth + 1;
    
    I0(1, length(N0)) = ibest;
    J0(1, length(N0)) = jbest;
    [~, ~, ~, ~, image_bottom_left] = best_paired_comp_tree_top(x, I0, J0, N0, prior0, exclusions, manual, depth, img_files_path, img_files, ids);
    I0(1, length(N0)) = jbest;
    J0(1, length(N0)) = ibest;
    [~, ~, ~, ~, image_bottom_right] = best_paired_comp_tree_top(x, I0, J0, N0, prior0, exclusions, manual, depth, img_files_path, img_files, ids);
    
    sl = size(image_left);
    sr = size(image_right);
    image_bottom_left = imresize(image_bottom_left, [sl(1), sl(2)]);
    image_bottom_right = imresize(image_bottom_right, [sr(1), sr(2)]);
    tree_image = [image_left image_right; image_bottom_left image_bottom_right];
else
    image_bottom_left = 0 * image_left;
    image_bottom_right = 0 * image_right;
    tree_image = [image_left image_right; image_bottom_left image_bottom_right];
end






