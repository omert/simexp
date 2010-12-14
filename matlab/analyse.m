function analyse(x, d)

[U, S, V] = svds(x, d);

P = V * S^(-1);

plot_results(U);
return;

[Uh Sh Vh] = svd(H);

dg = diag(Sh);
I = find(dg > max(dg) / 1000); 
J = find(dg <= max(dg) / 1000);
dg(I) = 1./dg(I);
dg(J) = 0;
Sh = diag(dg);

C = Vh * Sh * Uh' / 2;

[N d] = size(x);
E = zeros(size(U));
for i = 1:N
    for j = 1:d
        Pj = zeros(length(C), 1);
        for k = 1:d
            Pj(i + (j - 1) * N) = P(j, k);
        end
        E(i, j) = Pj' * C * Pj;
    end
end


plot_results