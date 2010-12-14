h = figure(1);
set(h, 'PaperPosition', [0 0 140 70]);
c = listfonts;
hold on
x = 1;
num_font = length(c);
height = 0.1;
for i=1:num_font
    clf;
    hold on
    h(1) = text(0, 2 * height, 'The quick brown');
    h(2) = text(0, height, 'fox jumps over');
    h(3) = text(0, 0, 'the lazy dog.');
    hold off;
    for j=1:3
        set(h(j), 'fontname', c{i});
    end
    axis([0.1 1 -0.1 0.3])
    axis off
    print('-djpeg90', ['.\fonts\' c{i}]);
end
