function [ count , clusters ] = scanclusters( w )

% over one dim for now

[m,n,~] = size(w);
[uq,~,inds] = unique(round(w(:,:,1)*100));
count = size(uq,1);
clusters = reshape(inds,m,n);

end

