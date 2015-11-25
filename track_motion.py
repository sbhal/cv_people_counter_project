# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 23:50:30 2015

@author: siddh
"""

import sys
#sys.path.append("C:\Users\siddh\Desktop\people_counting_python_opencv-master\opencv_start_kit")
sys.path.append("opencv_start_kit")

import cv2
#from cv2.cv import *
#import cv2.cv as cv
import math
import numpy as np
from scipy import misc

global target_dict

class Tracking:
    def __init__(self):
        self.max_distance_between = 50 #10
        self.min_distance_between = 0 #5
        self.tracks_id = 0
        self.list_of_tracks = []
        self.list_of_points = []
        self.first_point = False
        self.up = 0
        self.down = 0

    def find_nearest_track(self, point):
        point_with_no_track = ()
#        print "find_nearest_track entered with point ", point
        flag_added = False
        if len(self.list_of_tracks) >= 1:
            for track in self.list_of_tracks:
#                if len(track) != 0:
                last_index_of_track = len(track)-1
                last_element_coord_list = track[last_index_of_track]
                last_element_coord = last_element_coord_list[-1]
                last_coord_x = last_element_coord[0]
                last_coord_y = last_element_coord[1]
                distance_between = math.hypot(last_coord_x - point[0], last_coord_y - point[1])
#                print "distance wrt track ", track[0], " is ", distance_between
                if (distance_between < self.max_distance_between) and (distance_between >= self.min_distance_between):
#                   track.append(point)
#                    print "yay !"
                    flag_added = True
                    if (last_element_coord != point):
                        if point[1] >= 142 and last_coord_y < 142 and track[1] == False:
                            self.down = self.down+1
#                            cv2.putText(color_image, "up", (0, self.frame_height/2 - 5), cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.0, color=(250, 0, 0))

                        if point[1] <= 142 and last_coord_y > 142 and track[1] == False:
                            self.up = self.up+1
#                            cv2.putText(color_image, "down", (0, self.frame_height / 2 + 25), cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.0, color=(250, 0, 0))

                        last_element_coord_list.append(point)
            if flag_added == False:
                point_with_no_track = point
        else:
            point_with_no_track = point
            self.first_point = True
        return self.first_point, point_with_no_track

    def add_points_to_tracks(self, point):
        self.first_point, point_with_no_track = self.find_nearest_track(point)
        if point_with_no_track:
#            print "adding new track"
            if self.first_point:
                self.tracks_id += 1
                track = ("track %d" % self.tracks_id, False,  [point])
                self.list_of_tracks.insert(0, track)
                self.first_point = False
            else:
                self.tracks_id += 1
                track = ("track %d" % self.tracks_id, False, [point])
                self.list_of_tracks.append(track)
#               print self.list_of_tracks


class Target:
    def __init__(self):
        self.capture = cv2.VideoCapture("People.mp4")
        retval, self.frame = self.capture.read()
        self.frame_size = self.frame.shape
        print  "self frame shape is ", self.frame.shape
        self.grey_image = np.zeros(self.frame.shape, np.uint8)# cv2.CreateImage(self.frame_size, cv2.IPL_DEPTH_8U, 1)
        self.moving_difference = np.zeros(self.frame.shape, np.uint8)
        self.background_img = np.zeros(self.frame.shape, np.uint8)
        self.moving_average = np.zeros(self.frame.shape, np.uint32)# cv2.CreateImage(self.frame_size, cv2.IPL_DEPTH_32F, 3)
        self.min_area = 1800 #1800
        self.frame_width = self.frame_size[1]
        self.frame_height = self.frame_size[0]
#        self.list_of_points = []
        self.list_of_points = ()
        self.while_iteration = 0
        self.run_itr = 0

    def image_difference(self, first, method):
#        global background_img, moving_difference
        retval, color_image = self.capture.read()
        if first:
            self.moving_difference = np.copy(color_image)
            self.background_img = np.copy(color_image)
            first = False
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
        if method == 1:
            self.moving_difference = cv2.absdiff(color_image, self.background_img)
            self.grey_image = cv2.cvtColor(self.moving_difference, cv2.COLOR_BGR2GRAY)#cv2.CV_RGB2GRAY
            retval, self.grey_image = cv2.threshold(self.grey_image, 70, 255, cv2.THRESH_BINARY)
    #        kernel = np.ones((11,11),'uint8')

#            self.grey_image = cv2.dilate(self.grey_image, kernel, iterations = 18) # 18 iterations
            self.grey_image = cv2.morphologyEx(self.grey_image, cv2.MORPH_OPEN, kernel, iterations = 5)
        elif method == 2:
            fgmask = self.fgbg.apply(color_image)
            fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel, iterations=5)
            retval, self.grey_image = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)

#        retval, labels = cv2.connectedComponents(self.grey_image)
        return color_image, first

    def find_if_close(self, cnt1,cnt2):
        row1,row2 = cnt1.shape[0],cnt2.shape[0]
        for i in xrange(row1):
            for j in xrange(row2):
                dist = np.linalg.norm(cnt1[i]-cnt2[j])
                if abs(dist) < 15 : #50
                    return True
                elif i==row1-1 and j==row2-1:
                    return False

    def add_contour_in_storage(self):
        #storage = cv2.mem CreateMemStorage(0)
#        contour = cv2.findContours(self.grey_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#        print "heir", len(contour)
#        cv2.findContours(self.grey_image, contour, heirarchy, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE, Point(0, 0))
        _ ,contours, heirarchy = cv2.findContours(self.grey_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#        contour, heirarchy = cv2.findContours(self.grey_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        LENGTH = len(contours)

        if LENGTH == 0:
            return contours
        else:
            status = np.zeros((LENGTH,1))

            for i,cnt1 in enumerate(contours):
                x = i
                if i != LENGTH-1:
                    for j,cnt2 in enumerate(contours[i+1:]):
                        x = x+1
                        dist = self.find_if_close(cnt1,cnt2)
                        if dist == True:
                            val = min(status[i],status[x])
                            status[x] = status[i] = val
                        else:
                            if status[x]==status[i]:
                                status[x] = i+1

            unified = []
            maximum = int(status.max())+1
            for i in xrange(maximum):
                pos = np.where(status==i)[0]
                if pos.size != 0:
                    cont = np.vstack(contours[i] for i in pos)
                    hull = cv2.convexHull(cont)
                    unified.append(hull)
    #        return contours
            return unified

    @staticmethod
    def get_rectangle_parameters(bound_rect, color_image):
        pt1 = (bound_rect[0], bound_rect[1])
        pt2 = (bound_rect[0] + bound_rect[2], bound_rect[1] + bound_rect[3])
        x_center = abs(pt1[0] - pt2[0]) / 2 + pt1[0]
        y_center = abs(pt1[1] - pt2[1]) / 2 + pt1[1]
        point = (x_center, y_center)
        y_length = abs(pt1[0] - pt2[0])
        x_length = abs(pt1[1] - pt2[1])
        area = x_length * y_length
        return pt1, pt2, point, area

    def get_points_tracking(self, point, area, color_image):
        if area > self.min_area:
            cv2.circle(color_image, center=point, radius=2, color=(255, 255, 0), thickness=6)
#            self.list_of_points.append(point)
            self.list_of_points = point
            global tracking_dict
            tracking_dict = tracking.__dict__
#            for point in self.list_of_points:
            tracking.add_points_to_tracks(point)

    def run(self):
        first = True
        self.run_itr = self.run_itr + 1
        print "Run iterantion is ", self.run_itr, " and last while itr was ", self.while_iteration
        self.while_iteration = 0
        self.fgbg = cv2.createBackgroundSubtractorMOG2()

        while True:
            self.while_iteration = self.while_iteration + 1
#            print "------>While Iteration is ", self.iteration
            color_image, first = self.image_difference(first, 2)
            contour = self.add_contour_in_storage()
            #font = cv2.InitFont(cv2.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 1, 1)
            cv2.line(color_image, (0, self.frame_height/2), (self.frame_width, self.frame_height/2), color=(250, 0, 0), thickness=1)
            cv2.putText(color_image, "In(%d)"%tracking.up, (0, self.frame_height/2 - 5), cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.0, color=(0, 0, 250))
            cv2.putText(color_image, "Out(%d)"%tracking.down, (0, self.frame_height / 2 + 25), cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.0, color=(0, 0, 250))
#            print "len of points    is ", len(self.list_of_points)
            for cnt in contour: #while contour:
                bound_rect = cv2.boundingRect(cnt)
                #contour = contour.h_next()
                pt1, pt2, point, area = self.get_rectangle_parameters(bound_rect, color_image)
                cv2.rectangle(color_image, pt1, pt2, (255, 0, 0), 1)
                self.get_points_tracking(point, area, color_image)
#                tracking = Tracking()
#                global tracking_dict
#                tracking_dict = tracking.__dict__
#                for point in self.list_of_points:
#                    tracking.add_points_to_tracks(point)
#            cv2.circle(color_image, (278,10), radius=5, color=(255, 255, 0), thickness=6)
            cv2.imshow("myOutput", color_image)

            c = cv2.waitKey(1) % 0x100
            if c == 27:
                break

        cv2.destroyAllWindows()


if __name__ == "__main__":
    t = Target()
    tracking = Tracking()
    t.run()