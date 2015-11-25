# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 23:50:30 2015

@author: siddh
"""

import numpy as np
import cv2

cap = cv2.VideoCapture("People.mp4")

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows = True)
#fgbg = cv2.createBackgroundSubtractorKNN()

while(1):
    ret, frame = cap.read()
    ret, frame2 = cap.read()

    fgmask = fgbg.apply(frame)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel, iterations=3)
    retval, thres = cv2.threshold(fgmask, 150, 255, cv2.THRESH_BINARY)
    retval, labels = cv2.connectedComponents(thres)
    cv2.imshow('background with shadow',fgmask)
    cv2.imshow('threshold',thres)
    output = np.zeros_like(labels, dtype=np.uint8)
    labels = labels + 1
    cv2.normalize(labels, output, 0 , 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
#    output.convertTo(imgResult, CV_8UC3);
#    cv2.convertScaleAbs()
    cv2.imshow('Input',frame)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()

#%%
output = np.empty_like(labels)
cv2.normalize(labels, output, 255 , 255, cv2.NORM_INF)