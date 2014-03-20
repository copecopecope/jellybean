function [ newimg ] = highlight_removal( img, method )

img = im2double(img);
newimg = img;
if strcmp(method, 'simple')
    newimg = remove_simple(img, .5);
end

end

function [ newimg ] = remove_simple(img, maxd)
    [m,n,~] = size(img);
    newimg = zeros(m,n,3);
    for i = 1:m
        for j = 1:n
            spec_term = (max(img(i,j,:)) - maxd*sum(img(i,j,:)))/(1-3*maxd);
            newimg(i,j,:) = img(i,j,:) - repmat(spec_term,[1 1 3]);
        end
    end  
    disp(newimg(28,34,:))
    newimg = im2uint8(newimg);
end


