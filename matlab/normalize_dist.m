function p = normalize_dist(p0, dim)

if nargin < 2
    dim = 1;
end
s = size(p0);
sm = sum(p0, dim);
if dim == 1
    p = p0 ./ repmat(sm, s(1), 1);
else
    p = p0 ./ repmat(sm, 1, s(2));
end
