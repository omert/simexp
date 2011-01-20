function plot_convergence(test1file, test2file, controlfile, dataset1name, dataset2name)

load(test1file);
fprintf('%d comparisions in dataset 1. \n', length(IX));
IX1 = IX;
IA1 = IA;
IB1 = IB;
N1 = N;

load(test2file);
fprintf('%d comparisions in dataset 2. \n', length(IX));
IX2 = IX;
IA2 = IA;
IB2 = IB;
N2 = N;

load(controlfile);
fprintf('%d comparisions in control dataset. model dimension %d\n', length(IX), min(size(x)));
xc = x;

max_sample_size = max([length(IX1), length(IX2)]);
sample_size = round(linspace(1000, max_sample_size, 4));
llh1 = [];
llh2 = [];

tic;
x1 = xc;
x2 = xc;
for i = 1:length(sample_size)
    ss = sample_size(i);
     I = 1:ss;
    if length(IX1) >= ss
        x1 = fit(x1, IX1(I), IA1(I), IB1(I), N1(I), 4);
        llh1(i) = -model_likelihood(x1, IX, IA, IB, N);
    end
    if length(IX2) >= ss
        x2 = fit(x2, IX2(I), IA2(I), IB2(I), N2(I), 4);
        llh2(i) = -model_likelihood(x2, IX, IA, IB, N);
    end
    plot(llh1, sample_size(1:length(llh1)) / 40 * 0.15, 'r', llh2, sample_size(1:length(llh2)) / 40 * 0.15, 'b');
    legend(dataset1name, dataset2name,'Location','NorthWest');
    drawnow;
    fprintf('done %d out of %d\n', i, length(sample_size));
    fprintf('expected time to finish: %.0f\n', (length(sample_size)^2-i^2) * toc / i^2);
end
save convergence_data
keyboard