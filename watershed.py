import cv2, math, sys, random
import numpy as np

def lut():
  lut = np.ones((256), dtype=np.uint8)
  for i in range(256):
    lut[i] = math.floor(i/2) if i < 50 else i
  return lut.view(dtype=np.uint8)

def disp_watershed(img, markers, outfile):
  # color tab for watershed
  colorTab = []
  for i in range(contCount):
    r = math.floor(random.random()*255)
    g = math.floor(random.random()*255)
    b = math.floor(random.random()*255)
    colorTab.append([r,g,b])

  wshed = np.zeros((h,w,3), dtype=np.uint8)
  for i in range(h):
    if i%50 == 0:
      print '#'
    for j in range(w):
      index = markers[i,j]
      if index == -1:
        wshed[i,j] = [255,255,255]
      if index <= 0 or index >= contCount:
        wshed[i,j] = [0,0,0]
      else:
        wshed[i,j] = colorTab[index]

  mixed = wshed*0.5 + img*0.5
  cv2.imwrite(outfile, mixed)


def watershed(fname):
  img_l = cv2.imread(fname)
  h,w,_ = img_l.shape
  img = cv2.resize(img_l, (w/4,h/4))
  h,w,_ = img.shape

  print h,w

  # convert to grayscale
  gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

  # adaptive histogram to increase contrast
  clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(32,32))
  gray_e = clahe.apply(gray)

  # dilate to remove noise
  str_e = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
  gray_f = cv2.dilate(gray_e, str_e)

  # lut to increase black levels
  gray_g = cv2.LUT(gray_f, lut())

  # adaptive threshold to isolate foreground objects
  gray_h = cv2.adaptiveThreshold(gray_g, 255, \
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 45, 6)

  # erode to separate regions
  gray_i = cv2.erode(gray_h, str_e)
  gray_i = cv2.erode(gray_i, str_e)

  # find contours of binary image
  cont, hier = cv2.findContours(gray_i.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

  # filter contours by area
  idx = 0
  contours = []
  while idx >= 0:
    area = cv2.contourArea(cont[idx]) 
    if (20 < area < 5000):
      contours.append(cont[idx])
    idx = hier[0][idx][0]

  # draw contours
  markers = np.zeros((h,w), dtype=np.int32)
  contCount = 0
  for i in range(len(contours)):
    contCount += 1
    cv2.drawContours(markers, contours, i, contCount, -1)
  print contCount

  cv2.watershed(img,markers)

  disp_watershed(img,markers,'wshed.jpg')

  # cv2.imshow('test', mixed)
  # cv2.waitKey()

if __name__ == "__main__":
  try:
    fname = sys.argv[1]
    watershed(fname)
  except:
    watershed('img/img1.jpg')
