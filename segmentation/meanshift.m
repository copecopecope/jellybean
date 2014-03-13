function [pts] = meanshift( img, h, window_size, max_num_iters, epsilon, percent_conv )

ws = fix(window_size/2);
[m,n,~] = size(img);
% pts = zeros(m, n, 5);
pts = zeros(m,n,3);

% Construct feature-spatial point set
for i = 1:m
    for j = 1:n
%         pts(i,j,:) = [i; j; img(i,j,1); img(i,j,2); img(i,j,3)];
        pts(i,j,:) = [i; j; img(i,j)];
    end
end

% Translate Kernel windows until convergence

converged = zeros(m,n);
numconverged = 0;

fprintf('Num rows: %d\n',m);
for k = 1:max_num_iters
    totalms = 0;
    for i = 1:m
        for j = 1:n 
            if (converged(i,j)==1) 
                continue
            end
%             minx = fix(max([1 i-ws])); maxx = fix(min([m i+ws])); % maxx = fix(min(m,i+ws));
%             miny = fix(max([1 j-ws])); maxy = fix(min([n j+ws]));
%             
%             subpts = pts(minx:maxx,miny:maxy,:);
%             subpts = reshape(subpts,[],5);

%             subpts = reshape(pts,[],5);
            subpts = reshape(pts,[],3);
            
%             xi = reshape(pts(i,j,:),1,5);
            xi = reshape(pts(i,j,:),1,3);
            xis = repmat(xi,size(subpts,1),1);

            gs = exp(-sum((subpts-xis).^2,2)./h^2);

            knum = sum(bsxfun(@times, subpts, gs),1);
            kden = sum(gs);
            ms = (knum./kden)-xi;
            totalms = totalms + sum(ms.^2);
            if sum(ms.^2) < epsilon
                converged(i,j) = 1;
                numconverged = numconverged + 1;
            end
%             pts(i,j,:) = reshape(reshape(pts(i,j,:),1,5)+ms,1,1,5);
            pts(i,j,:) = reshape(reshape(pts(i,j,:),1,3)+ms,1,1,3);
        end
        if mod(i,10) == 0
            fprintf('   Row %d scanned...\n',i)
        end
    end
    fprintf('ITER %d COMPLETE, sum of shifts: %f, percent converged: %f\n', k, totalms, numconverged/(m*n))
    if numconverged/(m*n) >= percent_conv
        break
    end
end

