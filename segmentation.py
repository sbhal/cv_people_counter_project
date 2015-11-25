#import cv2
#import cv2.cv as cv
#import numpy as np
#from matplotlib import pyplot as plt

#img = cv2.imread('plate.jpg',0)
#gray = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
#color = cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU
#ret, thresh = cv2.threshold(gray,0,255,color)

import numpy as np
import cv2
from matplotlib import pyplot as plt


cap = cv2.VideoCapture("People.mp4")

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7))
fgbg = cv2.createBackgroundSubtractorMOG2()
#fgbg = cv2.createBackgroundSubtractorKNN()

while(1):
    ret, img = cap.read()
    
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    
    cv2.imshow("image",thresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    # noise removal
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)
    
    # sure background area
    sure_bg = cv2.dilate(opening,kernel,iterations=3)
    
    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(opening, cv2.CV_DIST_L2, 5)
    cv2.CV_DIST_L2 
    ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)
    
    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg,sure_fg)
    
    #
    # Marker labelling
    #ret, markers = cv2.connectedComponents(sure_fg)
    
    # Add one to all labels so that sure background is not 0, but 1
    #markers = markers+1
    
    # Now, mark the region of unknown with zero
    #markers[unknown==255] = 0
    
    #markers = cv2.watershed(img,markers)
    #img[markers == -1] = [255,0,0]
    
    cv2.imshow("image",sure_fg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cv2.imshow("image",unknown)
    cv2.waitKey(0)
    cv2.destroyAllWindows()