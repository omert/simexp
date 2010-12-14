function fit_feature(x, f0, fig, ttl)
figure(fig);
clf(fig);
num_plots = 1;

x1 = [x 100*ones(26, 1)];
f = zeros(size(f0));

ridge_param = 1;

for i = 1:26
    x2 = x1;
    x2(i, :) = [];
    f2 = f0;
    f2(i) = [];
    y = pinv(x2' * x2 + ridge_param * eye(size(x2' * x2))) * x2' * f2;
    v1 = x1 * y;
    f(i) = v1(i);
end
subplot(1, 1, 1);
axis([1 26 min([f; f0]) max([f; f0])]);
axis off
line([1 26], [0 0]);
for i = 1:26
    handle = text(i, f0(i), char(i - 1 + 'a'));
    set(handle, 'color', [0 0 1]);
    text(i, f(i), char(i - 1 + 'a'));
end
c = corrcoef(f,f0);
title(sprintf('%s      c = %2f', ttl, c(1,2)));


