function feature_fit_graph

load('../turkexps/flags/random/all.data.mat');
[attributes names] = read_info('../data/flags/info.csv', ids);

num_samples = 40;
sample_sizes = (1:num_samples) * length(IX) / num_samples

for i = 1:num_samples
    I = 1:(sample_sizes(i));
    x = fit_mat_and_trace(IX(I), IA(I), IB(I), N(I), ids, 10);
    corrects(i) = check_features(attributes, names, x, ids, 'flags', ...
                                 '../data/flags/',4);
    save feature_graph sample_sizes corrects
end
plot(sample_sizes, corrects / length(ids));