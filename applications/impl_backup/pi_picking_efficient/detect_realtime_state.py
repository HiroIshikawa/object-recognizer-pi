from detect import *
from measure import *
from interface import *
from preprocess import *
#opens up a webcam feed so you can then test your classifer in real time
#using detectMultiScale
from sys import argv
import sys
import cv2
import numpy as np
import time
import threading

from video import WebcamVideoStream
from fps import FPS

obj_w = int(argv[1])
obj_h = int(argv[2])
scale_factor = float(argv[3])
min_neighs = int(argv[4])
win_w = int(argv[5])
win_h = int(argv[6])


def command(avg_pos):
    if (avg_pos > 10):
        print("Turn Right: Rotate "+str(avg_pos)+" units")
    elif (avg_pos < -10):
        print("Turn Left: Rorate "+str(avg_pos)+" units")
    else:
        print("Go Straight")

def mean(l):
    if len(l)==0:
        return 0.0
    return sum(l)/len(l)

def navigate(candidates):
    threading.Timer(0.5, navigate, args=[candidates]).start()
    global track_flag
    global avg_pos
    if candidates:
        avg_pos = mean(candidates)
        track_flag = True
        candidates[:] = []
    else:
        pass

def manual():
    print("in manual mode")


# initialize the nvagation system for different position
# global track_flag
# global avg_pos
track_flag = False
monitor_flag = False
avg_pos = 0.
candidates = []
# navigate(candidates)

# # Start capturing
# WebcamVideoStream
# cap = cv2.VideoCapture(0)
# cap.set(3,win_w)
# cap.set(4,win_h)

vs = WebcamVideoStream(0,win_w,win_h).start()
# vs.stream.set(3,win_w)
# vs.stream.set(4,win_h)
# vs.start()
# allow the camera to warmup
time.sleep(.1)

# reading cascade
cascade = cv2.CascadeClassifier("cascade.xml")

start_time = time.time()
monitor_start_time = 0.

try:
    while(True):
        # ret, img = cap.read()
        img = vs.read()
        imshape = img.shape
        # vertices = np.array([[(0,imshape[0]),(0,int(imshape[0]/2)), 
        #     (int(imshape[1]),int(imshape[0]/2)), (imshape[1],imshape[0])]], dtype=np.int32)
        # cv2.imshow("Raw", img)
        # img = region_of_interest(img, vertices)
        # cv2.imshow("Preprocessed", img)
        rects, img = detect(img, scale_factor, min_neighs, obj_w, obj_h)
        img = box(rects, img)
        cv2.imshow("Cascaded", img)
        measure(img, rects, candidates)


        # def navigate(candidates):
        if (time.time() - start_time > .5):
            # threading.Timer(0.5, navigate, args=[candidates]).start()
            # global track_flag
            # global avg_pos
            if candidates:
                avg_pos = mean(candidates)
                track_flag = True
                candidates[:] = []
                start_time = time.time()
            else:
                pass

        if track_flag:
            print("Tracking activated")
            track(avg_pos)
            # monitor_flag = True
            monitor_start_time = time.time()
            track_flag = False
            # time.sleep(.1)

        # if monitor_flag: 
        if time.time()-monitor_start_time < 5.:  # every time object detected, there's 5 secs window to keep runnning monitor()
            monitor(avg_pos)
            # monitor_flag = False
            # monitor_start_time = time.time()


        if cv2.waitKey(10) == 27:
            # time.sleep(1)
            print("Stopping..")
            vs.stop()
            cv2.destroyAllWindows()
            break


        # cv2.waitKey(1)
        # if(cv2.waitKey(1) & 0xFF == ord('q')):
            # break
        # if cv2.waitKey(1) & 0xFF == ord('q'):
except KeyboardInterrupt:
    vs.stop()
    cv2.destroyAllWindows()