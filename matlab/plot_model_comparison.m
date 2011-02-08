function plot_model_comparison(dataSetName)

load(['model_comparison_' dataSetName]);
name1 = [name1 ' triples'];
name2 = [name2 ' triples'];

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

sample_sizes = sample_sizes(1:length(ll1)) / length(x1{1}) + 1;

figure(4)
ax(1) = 9.9;
ax(2) = 36;
ax(3) = 3.1;
ax(4) = 5.4;
subplot(1,2,1);
title(dataSetName);
plot(sample_sizes, igain1(:, 3), 'r', sample_sizes, igain2(:, 3), 'k--');
legend(name1, name2, 'location', 'northeast');
title('20 Random Questions');
ylabel('log of rank in posterior');
xlabel('triples per object (training)');
%set(gca,'XDir','reverse')
axis(ax);

subplot(1,2,2);
title(dataSetName);
plot(sample_sizes, metrics1(:, 3), 'r', sample_sizes, metrics2(:, 3), 'k--');
legend(name1, name2, 'location', 'northeast');
title('20 Adaptive Questions');
xlabel('triples per object (training)');
%set(gca,'XDir','reverse')
axis(ax);
return

figure(1)
title(dataSetName);
plot(sample_sizes, ll1, 'r+-', sample_sizes, ll2, 'b.-');
legend(name1, name2, 'location', 'northeast');
title('Log Likelihood of Fit to Random Triples');
xlabel('Triples per Object');
%set(gca,'XDir','reverse')

figure(2)
title(dataSetName);
plot(sample_sizes, igain1(:, 1), 'r', sample_sizes, igain2(:, 1), 'b');
legend(name1, name2, 'location', 'northeast');
title('Bits of Information Learned from Random Triples');
xlabel('Triples per Object');

figure(3)
title(dataSetName);
plot(sample_sizes, igain1(:, 2), 'r', sample_sizes, igain2(:, 2), 'b');
legend(name1, name2, 'location', 'northeast');
title('Rank in Posterior, as Learned from Random Triples');
xlabel('Triples per Object');
%set(gca,'XDir','reverse')

figure(5)
title(dataSetName);
plot(sample_sizes, metrics1(:, 2), 'r', sample_sizes, metrics2(:, 2), 'b');
legend(name1, name2, 'location', 'northeast');
title('Rank in Posterior, as Learned from Adaptive Triples');
xlabel('Triples per Object');
%set(gca,'XDir','reverse')

% 1 866 899 5134 amex international travel

figure(7)
title(dataSetName);
plot(sample_sizes, metrics1(:, 1), 'r', sample_sizes, metrics2(:, 1), 'b');
legend(name1, name2, 'location', 'northeast');
title('Bits of Information Learned from Adaptive Triples');
xlabel('Triples per Object');

figure(8)
title(dataSetName);
plot(sample_sizes, 1-corrects1, 'r', sample_sizes, 1-corrects2, 'b');
legend(name1, name2, 'location', 'northeast');
title('Prediction Error Rate of Random Triples');
xlabel('Triples per Object');





length(sample_sizes)