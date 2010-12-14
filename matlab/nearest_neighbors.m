function I = nearest_neighbors(x, i, n)

xi = repmat(x(i, :), length(x), 1);
[~, I] = sort(sum((x - xi).^2, 2));
I = I(1:n);