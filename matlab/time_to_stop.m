function t = time_to_stop(x, P)


x = x / sum(x);
if x * x' == 1
    t = 0;
    return
end
[num_q, ~] = size(P);

tj = zeros(size(x));
for j=1:num_q
    xj = x .* P(j, :);
    pj = sum(xj);
    if pj > 0 && sum(xj > 0)
        x1 = xj / sum(xj);
        if norm(x1 - x) > 0
            tj(j) = tj(j) + pj * time_to_stop(x1, P);
        else
            tj(j) = inf;
        end
    end
    
    xj = x .* (1 - P(j, :));
    pj = 1 - sum(x .* P(j, :));
    if pj > 0 && sum(xj > 0)
        x1 = xj / sum(xj);
        if norm(x1 - x) > 0
            tj(j) = tj(j) + pj * time_to_stop(x1, P);
        else
            tj(j) = inf;
        end
    end
end
t = 1 + min(tj);
