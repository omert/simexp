function f = fit_feature_svm(x, f0)

opts = optimset('quadprog');
opts.maxIter = 40000;

n = length(x)
length(f0)
Irand = randperm(n);

K = round(linspace(1, n, 10));
for i=2:length(K)


    I = Irand(K(i -1):K(i));
    J = setdiff(Irand, I);



    svm_res = svmtrain(f0(J), x(J, :), '-t 0');
    f(I) = svmpredict(0*(1:length(I))', x(I, :), svm_res);

% $$$     svm_res = svmtrain(x(I, :), f0(I), 'QuadProg_Opts', opts);
% $$$     f(J) = svmclassify(svm_res, x(J, :));
% $$$     
% $$$     svm_res = svmtrain(x(J, :), f0(J), 'QuadProg_Opts', opts);
% $$$     f(I) = svmclassify(svm_res, x(I, :));
    
end
