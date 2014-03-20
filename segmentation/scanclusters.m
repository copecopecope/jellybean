function [ count , clusters, centroids, areas, variances] = scanclusters( w )

% over one dim for now

[m,n,~] = size(w);
[uq,~,inds] = unique(round(w(:,:,1)*100));
count = size(uq,1);
clusters = reshape(inds,m,n);

areas = zeros(count,1);
pt_sums = zeros(count,2);

for i=1:m
    for j = 1:n
        ind = clusters(i,j);
        areas(ind) = areas(ind)+1;
        pt_sums(ind,:) = pt_sums(ind,:)+[i,j];
    end
end

centroids = bsxfun(@rdivide, pt_sums, areas);
variances = bsxfun(@rdivide, norm(pt_sums-centroids), areas); 

% filter out "bad clusters"
goodinds = find(areas>30&variances<1000);
centroids = centroids(goodinds,:);
% areas = areas(goodinds);
% variances = variances(goodinds);

end

