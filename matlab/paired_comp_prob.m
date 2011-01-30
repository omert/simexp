function P = paired_comp_prob(beta, X, I, J)

%Y = (sum(X(I, :) .* X(I, :), 2) - sum(X(J, :) .* X(J, :), 2))/2;
%P = 1 ./ (1 + exp(- N .* ((X(I, :) - X(J, :)) * beta + Y)));

beta_size = size(beta);
num_vecs = beta_size(1);
P = zeros(length(I), num_vecs);

XI = X(I, :);
XJ = X(J, :);
for i = 1:num_vecs
    B = repmat(beta(i, :), length(I), 1);
    %    LLHR = row_norm(B - X(I, :)) - row_norm(B - X(J, :));
    %    LLHR = sum((B - X(J, :)).^2, 2) - sum((B - X(I, :)).^2, 2);
    % LLHR = sum(B * (X(I, :) - X(J, :))');
    
    %    LLHR = log(1 + sum((B - X(J, :)).^2, 2)) - log(1 + sum((B - X(I, :)).^2, 2));
    LLHR = log(1 + sum((B - XJ).^2, 2)) - log(1 + sum((B - XI).^2, 2));
    P(:, i) = sigmoid(LLHR);
end
