function M1 = projectPSD_rank(M, r)

sm = size(M);
if sm(1) == sm(2)
    
    M = (M + M')/2;
    [V D] = eig(M);
    d = diag(D);
    d = max(d, 0);
    if length(d) > r
        d(1:(length(d)-r)) = 0;
    end
    M1 = V * diag(d) * V';
else
    
    M = M * M';
    [V D] = eig(M);
    d = diag(D);
    d = max(d, 0);
    if length(d) > r
        tr = sum(d);
        d(1:(length(d)-r)) = 0;
        d = d * tr / sum(d);
        D = diag(sqrt(d));
        M1 = V * D(:, (end-r+1):end);
    else
        M1 = V * diag(sqrt(d));
    end
end
