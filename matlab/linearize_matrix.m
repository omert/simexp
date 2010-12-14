function v = linearize_matrix(V)

%v = V(:);
%return
[n1 n2] = size(V);
I = 1:n1;
J = 1:n2;
[I J] = meshgrid(I, J);
I = I';
J = J';
v = V(find(I > J));