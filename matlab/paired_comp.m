options = optimset('display', 'iter', 'maxfunevals', 10000);%, 'GradObj','on');

[num_obj d] = size(x);
beta = rand(d, 1);
I = ceil(rand(d, 1) * num_obj)
J = ceil(rand(d, 1) * num_obj)
return;
while 1
    
    beta = fminunc(@(beta) paired_comp_llh(beta, x, I, J, N), beta, options);
end
