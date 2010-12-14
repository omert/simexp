function R   = sparse_loss_lsq(V, IX, IA, IB, N, num_obj, d, dbg)

[V, params] = decode_params(V, num_obj, d);

%DA = row_norm(V(IX, :) - V(IA, :))/2;
%DB = row_norm(V(IX, :) - V(IB, :))/2;  % distance
DA = sum((V(IX, :) - V(IA, :)).^2, 2);
DB = sum((V(IX, :) - V(IB, :)).^2, 2);  % distance squared
%S = sum(V(IX, :) .* (V(IA, :) - V(IB, :)), 2); % dot product


LLHR = log(1 + DB) - log(1 + DA);
%LLHR = DB - DA;
%LLHR = -S; 
P = sigmoid(LLHR);
R = sqrt(- N .* log(P));
if nargin > 7
    keyboard
end
