function plot_model_comparison(dataSetName)

load(['model_comparison_' dataSetName]);

for i = 1:length(ll1)
    S1 = x1{i}*x1{i}';
    S2 = x2{i}*x2{i}';
    [ll1(i) corrects1(i) ] = mat_model_likelihood(S1, IXcontrol, ...
                                                 IAcontrol, IBcontrol, ...
                                                 Ncontrol);
    [ll2(i) corrects2(i) ] = mat_model_likelihood(S2, IXcontrol, ...
                                                 IAcontrol, IBcontrol, ...
                                                 Ncontrol);
end

sample_sizes = sample_sizes(1:length(ll1));

figure(1)
title(dataSetName);
plot(ll1, sample_sizes, 'r', ll2, sample_sizes, 'b');
legend(name1, name2);
title('Log likelihood of fit to control');
set(gca,'XDir','reverse')

figure(2)
title(dataSetName);
plot(igain1(:, 1), sample_sizes, 'r', igain2(:, 1), sample_sizes, 'b');
legend(name1, name2);
title('bits of information learned');

figure(3)
title(dataSetName);
plot(igain1(:, 2), sample_sizes, 'r', igain2(:, 2), sample_sizes, 'b');
legend(name1, name2);
title('position in posterior nearest neighbors');
set(gca,'XDir','reverse')

figure(4)
title(dataSetName);
plot(igain1(:, 3), sample_sizes, 'r', igain2(:, 3), sample_sizes, 'b');
legend(name1, name2);
title('log of position in posterior nearest neighbors');
set(gca,'XDir','reverse')

figure(5)
title(dataSetName);
plot(metrics1(:, 2), sample_sizes, 'r', metrics2(:, 2), sample_sizes, 'b');
legend(name1, name2);
title('position in posterior nearest neighbors, using bank');
set(gca,'XDir','reverse')

figure(6)
title(dataSetName);
plot(metrics1(:, 3), sample_sizes, 'r', metrics2(:, 3), sample_sizes, 'b');
legend(name1, name2);
title('log position in posterior nearest neighbors, using bank');
set(gca,'XDir','reverse')

figure(7)
title(dataSetName);
plot(metrics1(:, 1), sample_sizes, 'r', metrics2(:, 1), sample_sizes, 'b');
legend(name1, name2);
title('bit of information learned, using bank');

figure(8)
title(dataSetName);
plot(corrects1, sample_sizes, 'r', corrects2, sample_sizes, 'b');
legend(name1, name2);
title('Random triplets prediction accuracy');
