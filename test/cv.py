import cv2
import numpy as np

def countBlobs(fname):
  img1 = cv2.imread(fname,1)
  h,w,_ = img1.shape
  img_s = cv2.resize(img1, (w/4,h/4))

  himg = cv2.cvtColor(img_s, cv2.COLOR_BGR2HSV)
  print himg.shape
  hs = himg.copy()[:,:,:2]
  h,w,_ = hs.shape
  v = np.ones((h,w,1), dtype=np.uint8)*200
  hsv = np.concatenate((hs,v),axis=2)
  hsv_ = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
  print hsv.shape
  cv2.imshow("result", hsv_)
  cv2.waitKey(0)

if __name__ == "__main__":

  countBlobs('../img/img1.jpg') # straight on, large jar

