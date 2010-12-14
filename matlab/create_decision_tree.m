function create_decision_tree(filename, x, degree, depth, ids, cutoff)


f = fopen(filename, 'w');
tic;
create_decision_tree_recur([], ones(length(x), 1) / length(x), f, x, degree, depth, ids, [], cutoff);    
fclose(f);
toc