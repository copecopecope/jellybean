function [pts] = meanshift( img, h, max_num_iters, totalms_thresh, ndims, histcount )

% ws = fix(window_size/2);
[m,n,~] = size(img);
pts = zeros(m, n, ndims);
% pts = zeros(m,n,3);

% Construct feature-spatial point set
for i = 1:m
    for j = 1:n
        pts(i,j,:) = [round(i/m*histcount); round(j/n*histcount); round(img(i,j,1)*histcount); round(img(i,j,2)*histcount); round(img(i,j,3)*histcount)];
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
%             minx = fix(max([1 i-ws])); maxx = fix(min([m i+ws])); % maxx = fix(min(m,i+ws));
%             miny = fix(max([1 j-ws])); maxy = fix(min([n j+ws]));
%             
%             subpts = pts(minx:maxx,miny:maxy,:);
%             subpts = reshape(subpts,[],5);

            subpts = reshape(pts,[],ndims);
            
            xi = reshape(pts(i,j,:),1,ndims);
            xis = repmat(xi,size(subpts,1),1);

            gs = exp(-sum((subpts-xis).^2,2)./h^2);

            knum = sum(bsxfun(@times, subpts, gs),1);
            kden = sum(gs);
            ms = (knum./kden)-xi;
            totalms = totalms + sum(ms.^2);
            pts(i,j,:) = reshape(reshape(pts(i,j,:),1,ndims)+ms,1,1,ndims);
        end
        if mod(i,10) == 0
            fprintf('   Row %d scanned...\n',i)
        end
    end
    fprintf('ITER %d COMPLETE, sum of shifts: %f\n', k, totalms)
    if totalms < totalms_thresh
        break
    end
end

