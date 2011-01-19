function L = mat_model_likelihood(S, IX, IA, IB, N)

m = length(S);

iXX = IX + m * (IX-1);
iBB = IB + m * (IB-1);
iAA = IA + m * (IA-1);
iXB = IX + m * (IB-1);
iXA = IX + m * (IA-1);

pa = 1.0 + S(iXX) + S(iBB) - 2 * S(iXB);
pb = 1.0 + S(iXX) + S(iAA) - 2 * S(iXA);
%pa = exp(S(iXA));
%pb = exp(S(iXB));
L = -sum(N .* (log(pa) - log(pa + pb))) / length(IX) / log(2);
