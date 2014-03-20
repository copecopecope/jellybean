function [img] = dispclusters( count, clusters )

[m,n] = size(clusters);
cmap = hsv(count);
cmap = cmap(randperm(count),:);

img = zeros(m,n,3);
for i=1:m
    for j=1:n
        img(i,j,:) = reshape(cmap(clusters(i,j),:),1,1,3);
    end
end

end
