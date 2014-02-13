import cv2
import numpy as np

def countBlobs(fname):
  img1 = cv2.imread(fname,1)

  himg1 = cv2.cvtColor(img1, cv2.cv.CV_RGB2HSV)

  cv2.imshow("result", img1)
  cv2.waitKey()

if __name__ == "__main__":

  countBlobs('../img/img1.jpg') # straight on, large jar

