import cv2,sys
import numpy as np

def countBlobs(fname):
  img = cv2.imread(fname,1)
  h,w,_ = img.shape

  himg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
  print himg.shape
  hs = himg.copy()[:,:,:2]
  h,w,_ = hs.shape
  v = np.ones((h,w,1), dtype=np.uint8)*200
  hsv = np.concatenate((hs,v),axis=2)
  hsv_ = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
  print hsv.shape
  cv2.imwrite('hs.jpg',hsv_)

if __name__ == "__main__":

  countBlobs(sys.argv[1]) # straight on, large jar

