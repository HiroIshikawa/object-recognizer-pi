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

def check_detection(candidates):
    threading.Timer(0.1, check_detection, args=[candidates]).start()
    global track_flag
    global avg_pos
    if candidates:
        avg_pos = mean(candidates)
        track_flag = True
        candidates[:] = []
    else:
        pass

# initialize the nvagation system for different position
global track_flag
global avg_pos
track_flag = False
avg_pos = 0.
candidates = []
check_detection(candidates)

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (win_w, win_h)
camera.framerate = 64
rawCapture = PiRGBArray(camera, size=(win_w, win_h))

# allow the camera to warmup
time.sleep(.1)

init_rawCapture = PiRGBArray(camera, size=(win_w, win_h))

# the time of the initiation
# start = time.time()

# while(True):
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    flag = False
    img = frame.array
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

    if track_flag:
        print("track activated")
        track(avg_pos)
        track_flag = False
        time.sleep(.1)
        # start = time.time() # since object found rest timer



    rawCapture.truncate(0)
    if(cv2.waitKey(1) & 0xFF == ord('q')):
	   break
