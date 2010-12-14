defaultStream.State = savedState;
%options = optimset('display', 'none', 'maxfunevals', 10000, 'GradObj','on','hessian','on', 'derivativecheck', 'on');
options = optimset('display', 'off', 'tolfun', 1e-16, 'maxfunevals', 10000, 'GradObj','on', 'derivativecheck', 'off', 'hessian', 'on');

[num_obj d] = size(x);
%[U,S,V] = svds(x, d);
%T = V' * S^(-1);

T = eye(d);

figure(1);
clf;
plot_results(x);

beta = linspace(0, 1, d).^2;
beta = beta(:);

I = ceil(rand(max(d + 5, 10), 1) * num_obj);
J = I(randperm(length(I)));
N = [];

letter = 'r';
gamma = x(letter - 'a' + 1, :)';

thandle = [];
for iter = 1:500
    tic;
    while length(I) > length(N)
        q = length(N) + 1;
%        question = sprintf('is it more like %c or %c? ', 'a'-1+I(q), 'a'-1+J(q));
%        N(q, 1) = input(question);
        p = paired_comp_prob(gamma, x, I(q), J(q), 1);
        if rand < p
            N(q, 1) = 1;
        else
            N(q, 1) = -1;
        end
    end
    [beta, FVAL, EXITFLAG, OUTPUT, grad, H] = fminunc(@(beta) paired_comp_llh(beta, x, I, J, N), rand(size(beta)), options);
    if isinf(beta(1))
        return
    end
    
    C = pinv(H + 0.001*eye(size(H)))/2;
%    hold on;
    for i=1:length(thandle)
        delete(thandle(i));
    end
    thandle = [];
    figure(1);
    for i=1:1
        ii = (i-1) * 2 + 1;
        jj = (i-1) * 2 + 2;
        Ci = C([ii, jj], [ii, jj]);
        [Vi Di] = eigs(Ci);
        Di = diag(Di);
        [dummy, imax] = max(Di);
        ang = atan2(Vi(2, imax), Vi(1, imax));
        xpos = beta(ii);
        ypos = beta(jj);
        thandle(end+1) = ellipse(sqrt(Di(imax)), sqrt(Di(3 - imax)), ang, xpos, ypos);
        subplot(1, 1, i);
        thandle(end+1) = text(xpos, ypos, letter);
        set(thandle(end),'color',[1 0 0])
        thandle(end+1) =  line(x([I(end) J(end)], ii), x([I(end) J(end)], jj));
    end
    figure(2);
    dist = row_norm(x - repmat(beta', num_obj, 1));
    plot(1:num_obj, dist, '.')
    for i=1:num_obj
        text(i, dist(i), sprintf('%c', 'a' - 1 + i));
    end
    
    detC = det(C)^(1/d);
    subplot(1, 1, 1);
    title(sprintf('%d    det(C)^{(1/d)} = %f', length(N), detC));
    drawnow;
    
    
    if detC < 0.01
        break;
    end

    i = ceil(rand * num_obj);
    j = ceil(rand * num_obj);
    p =  0.5;
    [i j p] = best_paired_comp(beta, x, I, J, N, C);
    fprintf('comparing with %c and %c. prob %f\n', 'a' - 1 + i, 'a' - 1 + j, p);
    I(length(I) + 1) = i;
    J(length(J) + 1) = j;
end

figure(3);
clf;
plot_logp(beta, x, I, J, N);