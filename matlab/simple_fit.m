num_obj = length(ids);
x = zeros(num_obj);
for i = 1:length(IX)
    x(IX(i), IA(i)) = x(IX(i), IA(i)) + 1;
    x(IA(i), IX(i)) = x(IA(i), IX(i)) + 1;

    x(IX(i), IB(i)) = x(IX(i), IB(i)) - 1;
    x(IB(i), IX(i)) = x(IB(i), IX(i)) - 1;
end

for i=1:min(size(x))
    x(:, i) = x(:, i) - mean(x(:, i));
end

imagesc(x);


