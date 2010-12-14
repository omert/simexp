function plot_results(U)

%E1 = sqrt(E);
num_subs = 1;
for f = 1:num_subs
    subplot(num_subs, 1, f);
    e1 = 2 * f - 1;
    e2 = 2 * f;
    axis([min(U(:, e1)) max(U(:, e1)) min(U(:, e2)) max(U(:, e2))]);
    hold on;
    for i = 1:length(U)
        text(U(i, e1), U(i, e2), char(i - 1 + 'a'));
%        line(U(i, e1) + [-E1(i, e1) E1(i, e1)], [U(i, e2) U(i, e2)]);
%        line([U(i, e1) U(i, e1)], U(i, e2) + [-E1(i, e2) E1(i, e2)]);
    end
    hold off;
end