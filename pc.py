__author__ = 'timur'
from cv2 import MORPH_RECT
#from cv2 import CV_CAP_PROP_POS_FRAMES
import numpy as np
import cv2

v = cv2.__version__
print "We work on",v, "version of cv2"
"""
# this part is checking all existing cameras
for i in range(-10,10):
    cap = cv2.VideoCapture(i)
    print i,"input has state",cap.isOpened()
#cap = cv2.VideoCapture(1)#video from webcam
#nFrame = cap.get(cv.CV_CAP_PROP_FRAME_COUNT) #frame number
"""
cap = cv2.VideoCapture("People.mp4")
disk1 = cv2.getStructuringElement(MORPH_RECT,ksize=(5,5))
disk3 = cv2.getStructuringElement(MORPH_RECT,ksize=(15,15))
disk2 = cv2.getStructuringElement(MORPH_RECT,ksize=(23,23))
sum_Up=0
sum_Down=0
List=[]

#print nFrame

while(cap.isOpened()):
    ret, frame = cap.read()

    #print line on video
    cv2.line(frame,(0,200),(800,200),(255,0,0),4)
    #set custom video input resolution
    ret = cap.set(3,1280)
    ret = cap.set(4,720)

    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    u = cur_frame_number = cap.get(0)
    print cur_frame_number
    cur_bw=0

    for j in range(1,2):
        k = u+j-1
        bw3=0
        subs3=0
        cur_rgb = frame

    cv2.imshow('The window name',gray)
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()







