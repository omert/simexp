function [f, P, DA, DB]   = sparse_loss(X, IX, IA, IB, N)


%DA = row_norm(V(IX, :) - V(IA, :))/2;
%DB = row_norm(V(IX, :) - V(IB, :))/2;  % distance
DA = sum((X(IX, :) - X(IA, :)).^2, 2);
DB = sum((X(IX, :) - X(IB, :)).^2, 2);  % distance squared
%S = sum(V(IX, :) .* (V(IA, :) - V(IB, :)), 2); % dot product


LLHR = log(1 + DB) - log(1 + DA);
%LLHR = DB - DA;
%LLHR = -S; 
P = sigmoid(LLHR);
f = - sum(N .* log(P));
if nargin > 10
    keyboard
end
