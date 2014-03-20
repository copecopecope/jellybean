function [ct,cl,cs,goodcs,as,vs,climg] = ms( img, h, max_iters, thresh, histcount)
pts = meanshift(img, h, max_iters, thresh, 5, histcount);
[ct, cl, cs, goodcs, as, vs] = scanclusters(pts);
climg = dispclusters(ct,cl);
close all;
imshow(climg);
hold on
plot(cs(:,2),cs(:,1),'k+');
hold off
figure;
imshow(climg);
hold on
plot(goodcs(:,2),goodcs(:,1),'k+');
hold off
figure;
imshow(img);
hold on
plot(goodcs(:,2),goodcs(:,1),'k+');
hold off
figure;
imshow(climg);
end

