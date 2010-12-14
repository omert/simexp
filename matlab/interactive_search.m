function interactive_search(x, dataset, ids, img_files_path, human_input)

close all
figure(1);
hfig2 = figure(2);
pos = get(hfig2, 'position');
pos(1)=1120;
set(hfig2, 'position', pos);
[num_obj d] = size(x);
T = eye(d);


img_files = get_image_files(dataset);


I = [];
J = [];
N = [];


prior = ones(1, num_obj) / num_obj;

if human_input == 0
    computer_object = 5;
    gamma = x(computer_object, :);
end


for iter = 1:1000
    [inew jnew pnew kldiv tree_image] = best_paired_comp_tree_top(x, I, J, N, prior, [], 1, 0, img_files_path, img_files, ids);
    
    if human_input == 0 && (inew == computer_object || jnew == computer_object)
        return
    end

    figure(1);
    I(length(I) + 1) = inew;
    J(length(J) + 1) = jnew;
    
    
    q = length(N) + 1;
    image(tree_image);
    title(sprintf('query %d', iter));
    axis off;
    axis equal;

    fprintf('question %d. expecting answer (1) with probability %.3f\n', length(I), pnew);
    fprintf('is it more like\n (1) %s\n    or\n (2) %s\n> ', img_files{ids(I(q)) + 1}, img_files{ids(J(q)) + 1});
    
    N(q, 1) = 1;
    if human_input
        pause;
        button = get(gcf, 'currentkey');
        if sum(button) == sum('leftarrow')
            choice = 1;
        elseif sum(button) == sum('rightarrow')
            choice = -1;
        else
            choice = 0;
            if length(I) > 1
                prior(I(end-1)) = max(prior);
                prior(J(end-1)) = max(prior);
                prior = normalize_dist(prior);
                I = I(1:(end-2));
                J = J(1:(end-2));
                N = N(1:(end-2));
            else
                I = I(1:(end-1));
                J = J(1:(end-1));
                N = N(1:(end-1));
            end
        end
    else
        p = paired_comp_prob(gamma, x, I(q), J(q));
        fprintf('actual probability is %.3f\n', p);
        if rand < p
            choice = 1;
        else
            choice = -1;
        end
    end
    if choice ~= 0
        prior(I(q)) = 1e-100;
        prior(J(q)) = 1e-100;
        prior = prior / sum(prior);
    end
    if choice == -1
        temp = I(q);
        I(q) = J(q);
        J(q) = temp;
%        image_j = image_j * 2;
    elseif choice == 1
%        image_i = image_i * 2;
    else
%        image_j = image_j * 2;
%        image_i = image_i * 2;
    end
%    image([image_i image_j]);
    title(sprintf('query %d', iter));
    axis off;
    axis equal;
    drawnow;
    if ~human_input
        pause;
    end
    
    figure(2);
    LL = -paired_comp_llh(x, x, I, J, N) + log(prior);
    P = conditional_prob_from_ll(LL);
    [P Ip] = sort(P, 2, 'descend');
    
    num_results_x = 3;
    num_results_y = 3;
    num_results = num_results_x * num_results_y;
    images = cell(num_results_x, num_results_y);
    subplot(num_results_y, num_results_x, 1);
    for i = 1:num_results        
        subplot(num_results_y, num_results_x, i);
        images{i} = imread([img_files_path img_files{ids(Ip(i)) + 1}]);
        image(images{i});
        axis equal;
        axis off;
        title(sprintf('  %.3f  ', P(i)));
    end
    
        
%    figure(3);
%    beta = rand(1, d);
%    beta = fminunc(@(beta) paired_comp_llh(beta, x, I, J, N), beta);
%    plot(x(:, 1), x(:, 2), '.b', beta(1), beta(2), 'xr', [x(inew, 1) x(jnew, 1)], [x(inew, 2) x(jnew, 2)], 'k');
    
    
    
    drawnow
end

%figure(4);
%plot_logp(beta, x, I, J, N)