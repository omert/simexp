function handles = show_all_objects(img_data, dataset, I, f)


sn = ceil(sqrt(length(I)));
clf;
for i = 1:length(I)
    xpos(i) = floor((i - 1) / sn) / sn;
    ypos(i) = mod(i - 1, sn) / sn;
    if nargin > 3
        xpos = (xpos + f(I(i))) / 2;
        subplot('position', [xpos(i) ypos(i) 1/sn/2 1/sn]);
    else
        subplot('position', [xpos(i) ypos(i) 1/sn 1/sn]);
    end
    try
        handles(I(i)) = subimage(img_data{I(i)});
    catch me
    end
    axis off;
   
end

