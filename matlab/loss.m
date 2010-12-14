function [f, g, pHist]   = loss(V, N, num_obj, d)

[V, params] = decode_params(V, num_obj, d);

gamma = 0;

m = max(size(N));
S = V * V';
Sii = repmat(diag(S), 1, m);
D = sqrt(Sii - 2 * S + Sii' + gamma)/2;
pHist = [];
Gamma = zeros(num_obj, num_obj);
f = 0;
for i = 1:m
    Di = repmat(D(i, :), m, 1);
    Si = repmat(S(i, :), m, 1);
%    LLHR = Si - Si';
    LLHR = (Di.^2)' - Di.^2;
    P = sigmoid(LLHR);

    if nargout > 2
        pHist = [pHist; P(:)];
    end
    %P = (1.0001 + erf(Di - Di')) / 2;
    Ni = reshape(N(:, :, i), m, m);
    P(:, i) = 1;
    P(i, :) = 1;
    Ni(:, i) = 0;
    Ni(i, :) = 0;
    Ni = Ni .* (1-eye(size(Ni)));
    L = Ni .* log(P);
    f = f - sum(L(:));
    if nargout > 1
        G = Ni .* P';
        G = G - G';
        Gamma(i, :) = sum(G, 2);
    end
end
if nargout > 1
  
%  g = (Gamma + Gamma') * V;
  g = zeros(size(V));
  for m = 1:num_obj
      for i = 1:num_obj
          if i ~= m
%              g(m, :) = g(m, :) - 0.5*(Gamma(m, i) + Gamma(i, m)) * (V(m, :) - V(i, :)) / sqrt(sum((V(m, :) - V(i, :)).^2) + gamma);
              g(m, :) = g(m, :) - 0.5 * (Gamma(m, i) + Gamma(i, m)) * (V(m, :) - V(i, :));
          end  
      end
  end
  g = g(:);
  %g = linearize_matrix(g);
end



