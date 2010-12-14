function plot_logp(beta, x, I, J, N)

n = 200;
xvec = linspace(min(x(:, 1)), max(x(:, 1)), n);
yvec = linspace(min(x(:, 2)), max(x(:, 2)), n);
[xvec yvec] = meshgrid(xvec, yvec);
logP = zeros(size(xvec));
for i = 1:n
    for j = 1:n
        beta(1) = xvec(i, j);
        beta(2) = yvec(i, j);
        logP(i, j) = -sum(log(paired_comp_prob(beta, x, I, J, N)));
    end
end
minP = min(logP(:));
maxP = max(logP(:));
contour(xvec, yvec, logP, [minP:0.05:(minP+1) (minP+2):maxP]);
hold on;
plot(x(:, 1), x(:, 2), '.b');

hold off;
    
    