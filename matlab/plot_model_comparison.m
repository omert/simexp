function plot_model_comparison(dataset)

load(['model_comparison_' dataset]);
figure(1)
title(dataset);
plot(sample_sizes, ll1, 'r', sample_sizes, ll2, 'b');
legend(name1, name2);
title('Log likelihood of fit to control');

figure(2)
title(dataset);
plot(sample_sizes, igain1(:, 1), 'r', sample_sizes, igain2(:, 1), 'b');
legend(name1, name2);
title('bits of information learned');

figure(3)
title(dataset);
plot(sample_sizes, igain1(:, 2), 'r', sample_sizes, igain2(:, 2), 'b');
legend(name1, name2);
title('position in posterior nearest neighbors');

figure(4)
title(dataset);
plot(sample_sizes, igain1(:, 3), 'r', sample_sizes, igain2(:, 3), 'b');
legend(name1, name2);
title('log of position in posterior nearest neighbors');