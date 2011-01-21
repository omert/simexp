function c = comma_separate(s)


s = [',' s ','];
I = find(s == ',');

c = cell(length(I) - 1, 1);

for iI = 2:length(I)
    i = I(iI - 1) + 1;
    j = I(iI) - 1;
    c{iI - 1} = s(i:j);
end
    