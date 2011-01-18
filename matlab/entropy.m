function h = entropy(P, dim)
% entropy function

if nargin < 2
    dim = 2;
end
h = - sum(P .* log(P + eps), dim);