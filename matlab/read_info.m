function [f names] = read_info(info_file_name)

lines = textread(info_file_name, '%s%*[^\n]');

if length(lines) < 2
    return;
end
    
header = comma_separate(lines{1});
atts = [];
names = {};
for i = 1:length(header)
    if length(header{i}) >= 4 & header{i}(1:4) == 'att_'
        atts = [atts i];
        names{end + 1} = header{i}(5:end);
    end
end

f = [];

for i = 2:length(lines)
    fields = comma_separate(lines{i});
    id = sscanf(fields{1}, '%f') + 1;
    if length(fields) == length(header)
        for j = 1:length(atts)
            f(id, j) = sscanf(fields{atts(j)}, '%f');
        end
    end
end


