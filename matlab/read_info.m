function [f names] = read_info(info_file_name, ids)

lines = textread(info_file_name, '%s%*[^\n]');
length(lines)
if length(lines) < 2
    return;
end
    
header = comma_separate(lines{1});
atts = [];
names = {};
id_field = 1;
for i = 1:length(header)
    if length(header{i}) >= 4 & header{i}(1:4) == 'att_'
        atts = [atts i];
        names{end + 1} = header{i}(5:end);
    end
    if strcmp(header{i}, 'id')
        id_field = i;
    end
end

f = [];

for i = 2:length(lines)
    fields = comma_separate(lines{i});
    id = sscanf(fields{id_field}, '%f');
    if length(fields) == length(header)
        for j = 1:length(atts)
            k = find(ids == id);
            if length(k) == 1
                f(k, j) = sscanf(fields{atts(j)}, '%f');
            end
        end
    end
end


