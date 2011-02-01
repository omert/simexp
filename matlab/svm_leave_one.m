function f = svm_leave_one(x, f0)


Iclassed = find(f0 > -1);

f0 = -ones(size(f0));

for i=1:length(Iclassed)

    
    j = Iclassed(i);
    J = setdiff(1:length(x), j);

    svm_res = svmtrain(f0(J), x(J, :), '-t 0');
    f(j) = svmpredict(0*(1:length(j))', x(j, :), svm_res);

% $$$     svm_res = svmtrain(x(I, :), f0(I), 'QuadProg_Opts', opts);
% $$$     f(J) = svmclassify(svm_res, x(J, :));
% $$$     
% $$$     svm_res = svmtrain(x(J, :), f0(J), 'QuadProg_Opts', opts);
% $$$     f(I) = svmclassify(svm_res, x(I, :));
    
end
