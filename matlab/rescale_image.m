function new_image = rescale_image(im, scale)

si = size(im);
si(1:2) = floor(si(1:2) ./ scale);
new_image = uint8(zeros(si));
for i = 1:si(1)
    for j = 1:si(2)
        i1 = (i-1) * scale + 1;
        j1 = (j-1) * scale + 1;
        I = i1:(i1 + scale - 1);
        J = j1:(j1 + scale - 1);
        new_image(i, j, :) = mean(mean(im(I, J, :), 1), 2);
    end
end
