function M1 = projectPSD_trace(M, max_trace)

% Project to positive semidefinites. M assumed to be symmetric
M = (M + M')/2;
[V D] = eig(M);

d = diag(D);
d = max(d, 0);
tr = sum(d);
if tr > max_trace
    dtr = cumsum(d) + d .* ((length(d)-1):-1:0)';
    I = find(dtr <= tr - max_trace);
    if ~isempty(I)
        i = I(end);
        d = max(0, d - d(i));
        dtr = dtr(i);
    else
        i = 0;
        dtr = 0;
    end
    d = max(0, d - (tr - max_trace - dtr) / (length(d) - i));
end
D = diag(d);

M1 = V * D * V';
M1 = (M1 + M1')/2;
