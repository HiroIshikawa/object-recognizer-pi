from detect import *
from interface import *
from measure import *
from preprocess import *
#opens up a webcam feed so you can then test your classifer in real time
#using detectMultiScale
from sys import argv
import sys
import cv2
import numpy as np
import time
import threading

from picamera.array import PiRGBArray
from picamera import PiCamera

from video_pi import PiVideoStream

obj_w = int(argv[1])
obj_h = int(argv[2])
scale_factor = float(argv[3])
min_neighs = int(argv[4])
# Change resolution to have better precision
win_w = 960
win_h = 240


def mean(l):
    if len(l)==0:
        return 0.0
    return sum(l)/len(l)

track_flag = False
avg_pos = 0.
candidates = []

vs = PiVideoStream((win_w,win_h),64).start()
time.sleep(2.0)

start_time = time.time()
monitor_start_time = 0.

while(True):
    img = vs.read()
    # cv2.imshow("Raw", img)
    # img = preprocess(img)
    # cv2.imshow("Preprocessed", img)
    rects, img = detect(img, scale_factor, min_neighs, obj_w, obj_h)
    img = box(rects, img)
#    cv2.imshow("Cascaded", img)
    measure(img, rects, candidates)

    # if there's no rects found, look around
    # if not rects:
    #     look_around() 
        # Check time elapsed, if over 10 sec, invoke spiral search
        # if (time.time()-start) > 10:
        #     spiral_search()
    #if (time.time()-start_time >.1):

    if True:  # if time.time() - start_time > 5:
        if candidates:
            avg_pos = mean(candidates)
            track_flag = True
            candidates[:] = []
            start_time = time.time()
        else:
            pass

    if track_flag:
        print("track activated")
        track(avg_pos)
        monitor_start_time = time.time()
        track_flag = False

    if time.time()-monitor_start_time < 5.:
        monitor(avg_pos)

    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break
