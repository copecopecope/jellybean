function [clusters ] = meanshift( img, h )

[m,n,~] = size(img);
pts = zeros(m*n, 5);

% Construct feature-spatial point set
for i = 0:m-1
    for j = 1:n
        pts(i*n+j,:) = [i+1; j; img(i+1,j,1); img(i+1,n,2); img(i+1,j,3)];
    end
end

% Initialize windows at points
windows = pts;

% Translate Kernel windows until convergence

for i = 1:m*n
    if mod(i,n) == 0
        disp('Row scanned...')
    end
    knum = 0;
    kden = 0;
%     for j = 1:m*n
%         g = exp(sum((pts(j)-pts(i)).^2)/h^2);
%         knum = knum + g*pts(j);
%         kden = kden + g;
%     end
    xis = repmat(pts(i,:),m*n,1);
    gs = exp(-sum((pts-xis).^2,2)./h^2);
    knum = sum(bsxfun(@times, pts, gs),1);
    kden = sum(gs);
    windows(i,:) = knum./kden;
end

