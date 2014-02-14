import cv2, math, sys, random
import numpy as np

def lut():
  lut = np.ones((256), dtype=np.uint8)
  for i in range(256):
    lut[i] = math.floor(i/2) if i < 50 else i
  return lut.view(dtype=np.uint8)

def disp_watershed(img, markers, contCount, outfile):
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

  mixed = wshed*0.5 + img_gray*0.5
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

  avg_area = 0
  num_beans = 0

  for i in wshed_areas:
    area = wshed_areas[i]['size']
    if area < 400 or area > 1000:
      continue

    max_x = -1
    min_x = -1
    max_y = -1
    min_y = -1
    for x,y in wshed_areas[i]['x']:
      if max_x < 0 or x > max_x:
        max_x = x
      if min_x < 0 or x < min_x:
        min_x = x
      if max_y < 0 or y > max_y:
        max_y = y
      if min_y < 0 or y < min_y:
        min_y = y
    width = max_x-min_x
    height = max_y-min_y

    avg_area += area
    num_beans += 1

    print i, area, width, height

  avg_area /= num_beans
  print avg_area

  # MARK: Look at the last 20 lines of code.
  # I'm calculating all the segments found by watershed
  # with jelly-bean sized area (400 < area < 1000).
  # Your task: filter out the ones with non-jellybean-shaped
  # bounding rectangles (i.e. width >> height or vice versa)
  # then find the beans with coords at lower left and upper right of image
  # use their areas to approx number of beans on the front 
  # face of the cylindrical jar. Text me with questions.
  # I can try to update the latex doc with an explanation of what
  # we've done so far with the figure


  disp_watershed(img,markers,contCount,'wshed.jpg')
  # cv2.imshow('test', mixed)
  # cv2.waitKey()

if __name__ == "__main__":
  try:
    fname = sys.argv[1]
    watershed(fname)
  except:
    watershed('img/img1.jpg')
