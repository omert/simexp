function [L percent_right expected_L] = mat_model_likelihood(S, IX, IA, IB, N)

m = length(S);

iXX = IX + m * (IX-1);
iBB = IB + m * (IB-1);
iAA = IA + m * (IA-1);
iXB = IX + m * (IB-1);
iXA = IX + m * (IA-1);

pa = 1.0 + S(iXX) + S(iBB) - 2 * S(iXB);
pb = 1.0 + S(iXX) + S(iAA) - 2 * S(iXA);

%pa = 2 * S(iXX) + S(iBB) - 2 * S(iXB);
%pb = 2 * S(iXX) + S(iAA) - 2 * S(iXA);

%pa = exp(S(iXA));
%pb = exp(S(iXB));

%pa = exp(S(iXX) - 2*S(iXB) + S(iBB));
%pb = exp(S(iXX) - 2*S(iXA) + S(iAA));
L = -sum(N .* (log(pa) - log(pa + pb))) / sum(N) / log(2);

if nargout > 1
    percent_right = length(find(pa > pb)) / length(IX);
end
if nargout > 2
    p = pa ./ (pa + pb);
    expected_L = -sum(N .* (p .* log(p) + (1 - p) .* log(1 - p))) / length(IX) ...
        / log(2);
end