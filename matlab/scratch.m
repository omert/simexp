
run_adaptive('../turkexps/neckties/small/random/','neckties',1,1);
return

load('c:\sim\turkexps\tiles\all.data.mat');
create_decision_tree('c:\sim\trees\tiles.tree9',x,9,3,ids);
load('c:\sim\turkexps\fonts\adaptive\all.data.mat')
create_decision_tree('c:\sim\trees\fonts.tree9',x,9,3,ids);
pause(3600 * 6);
load('c:\sim\turkexps\neckties\small\all.data.mat')
create_decision_tree('c:\sim\trees\neckties.tree9',x,9,3,ids);
load('c:\sim\turkexps\dogs\all.data.mat')
create_decision_tree('c:\sim\trees\dogs.tree9',x,9,3,ids);
return

tic;
while toc < 60
    i = ceil(rand*length(ids));
    I = nearest_neighbors(x, i, 60);
    x=fit(x, I, IX, IA, IB, N, 3);
end

return
h = figure(1);
pause;
c = get(h,'currentkey')


return
x=0.01:0.02:1;
y=x;
[x y] = meshgrid(x,y);
z = abs(1 - x - y);
t = zeros(size(x));
P = rand(3);
P = P ./ repmat(sum(P, 2), 1, length(P));
P = [P; 1 0 0; 1 0 1];
for i =  1:length(x)
    for j =  1:length(x)
        dist = [x(i,j), y(i,j), z(i,j)];
        t(i,j) = time_to_stop(dist, eye(3));
    end
end
imagesc(t);
return

P = ones(1,100);
P(1) = 1e-100;
P = P / sum(P);
Q=P;
Q(1)=0.9999999;
Q = Q/sum(Q);
KL_divergence(Q, P)
return

figure(10)
xvec = linspace(-30,30,1500);
eta = 2;
for z=logspace(-1,1,20)
    d1 = abs(xvec + z);
    d2 = abs(xvec - z);
    yvec1 = sigmoid(d1-d2);
    yvec2 = d1 ./ (d1 + d2);
    yvec3 = sigmoid(eta*log(eta+d1)-eta*log(eta+d2));
    plot(xvec, yvec1, 'r', xvec, yvec2, 'g', xvec, yvec3, 'b')
    axis([-30 30 0 1])
    z
    pause
end