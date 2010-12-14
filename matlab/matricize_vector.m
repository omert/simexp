function [V, k] = matricize_vector(v, num_obj, d)

%V = reshape(v, num_obj, d);
%return;
V = zeros(num_obj, d);
k = 1;
for j = 1:d
  for i = 1:num_obj
      if i > j
          V(i, j) = v(k);
          k = k + 1;
      end
  end
end
    

