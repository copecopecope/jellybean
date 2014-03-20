import cv2, math, sys, random
import numpy as np

def lut():
  lut = np.ones((256), dtype=np.uint8)
  for i in range(256):
    lut[i] = math.floor(i/5) if i < 50 else i
  return lut.view(dtype=np.uint8)

def save_watershed(img, markers, contCount, outfile):
  # color tab for watershed
  colorTab = []
  for i in range(contCount):
    r = math.floor(random.random()*255)
    g = math.floor(random.random()*255)
    b = math.floor(random.random()*255)
    colorTab.append([r,g,b])

  h,w,_ = img.shape

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

  img_ = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
  img_gray = cv2.cvtColor(img_,cv2.COLOR_GRAY2BGR)

  # mixed = wshed*0.5 + img_gray*0.5
  mixed = wshed
  cv2.imwrite(outfile, mixed)

  return mixed


def watershed(fname,outname):
  img = cv2.imread(fname)
  h,w,_ = img.shape
  # img = cv2.resize(img_l, (w/4,h/4))
  # h,w,_ = img.shape

  print h,w

  # convert to grayscale
  # gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
  gray = img.copy()[:,:,1]
  cv2.imwrite('gray.jpg', gray)

  # adaptive histogram to increase contrast
  clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(32,32))
  gray_e = clahe.apply(gray)

  # dilate to remove noise
  str_e = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
  gray_f = cv2.dilate(gray_e, str_e)

  # lut to increase black levels
  gray_g = cv2.LUT(gray_f, lut())
  # cv2.imshow('test', gray_g)
  # cv2.waitKey()


  # adaptive threshold to isolate foreground objects
  gray_h = cv2.adaptiveThreshold(gray_g, 255, \
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 99, 2)

  # cv2.imshow('test', gray_h)
  # cv2.waitKey()

  # erode to separate regions
  gray_i = cv2.erode(gray_h, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)))
  gray_i = cv2.erode(gray_i, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)))

  # cv2.imshow('test', gray_i)
  # cv2.waitKey()

  # add clusters found by meanshift

  # find contours of binary image
  cont, hier = cv2.findContours(gray_i.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

  # filter contours by area
  idx = 0
  contours = []
  while idx >= 0:
    area = cv2.contourArea(cont[idx]) 
    # print area
    if area > 3:
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
  print markers.max()

  wshed_areas = {}
  for i in range(-1,contCount+1):
    wshed_areas[i] = {}
    wshed_areas[i]['x'] = []
    wshed_areas[i]['size'] = 0

  # calculate areas of watershed contours (probably inefficient)
  
  for i in range(h):
    if i%50 == 0:
      print '#'
    for j in range(w):
      index = markers[i,j]
      wshed_areas[index]['x'].append([i,j])
      wshed_areas[index]['size'] = wshed_areas[index]['size']+1

  mixed = save_watershed(img,markers,contCount,outname)
  # cv2.imshow('test', mixed)
  # cv2.waitKey()

if __name__ == "__main__":
  if len(sys.argv) == 3:
    fname = sys.argv[1]
    outname = sys.argv[2]
    watershed(fname,outname)
  else: 
    watershed('img/img1.jpg', 'wshed.jpg')

