function [g dF BI BJ BIN BJN] = paired_comp_gradient(beta, X, I, J, N, P)

%    dX = X(I, :) - X(J, :);
%    g = -(N .* (1- P))' * dX;
    B = repmat(beta', length(I), 1);
    BI = B - X(I, :);
    BIN = repmat(row_norm(BI), 1, length(beta));
    BJ = B - X(J, :);
    BJN = repmat(row_norm(BJ), 1, length(beta));
%    dF = BI ./ BIN - BJ ./ BJN;
    dF = BI - BJ;
    g = -2 * (N .* (1- P))' * dF;
