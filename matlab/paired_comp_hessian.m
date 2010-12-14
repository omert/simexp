function H = paired_comp_hessian(beta, X, I, J, N, P)

[~, dF BI BJ BIN BJN] = paired_comp_gradient(beta, X, I, J, N, P);

H = zeros(length(beta));


%W = repmat((1-P) .* N, 1, min(size(X)));
%H = H - BI' * (W .* BI ./ BIN.^3);
%H = H + BJ' * (W .* BJ ./ BJN.^3);

%ddF2 = sum((1 - P) .* N .* (1 ./ BIN(:, 1) - 1./ BJN(:, 1)));
%H = H + ddF2 * eye(size(H));

W = repmat(-P .* (1 - P), 1, min(size(X)));
H = H + dF' * (W .* dF);
H = -H;



%g = paired_comp_gradient(beta, X, I, J, N, P);
%H = g' * g;

%dX = X(I, :) - X(J, :);
%P = paired_comp_prob(beta, X, I, J, N);
%V = P .* (1 - P);
%V = repmat(V, 1, min(size(X)));
%H = dX' * (V .* dX);
