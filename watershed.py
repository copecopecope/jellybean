import cv2
import numpy as np

def lut():
  lut = np.ones((256), dtype=np.uint8)*128


def watershed(fname):
  img_l = cv2.imread(fname)
  h,w,_ = img_l.shape
  img = cv2.resize(img_l, (w/4,h/4))

  # convert to grayscale
  gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

  # adaptive histogram to increase contrast
  clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(32,32))
  gray_e = clahe.apply(gray)

  # dilate to remove noise
  str_e = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
  gray_f = cv2.dilate(gray_e, str_e)

  # lut to increase black levels
  # gray_g = cv2.LUT(gray_f, lut())

  cv2.imshow('test', gray_g)
  cv2.waitKey()

if __name__ == "__main__":
  try:
    fname = sys.argv[1]
    watershed(fname)
  except:
    watershed('img/img1.jpg')
