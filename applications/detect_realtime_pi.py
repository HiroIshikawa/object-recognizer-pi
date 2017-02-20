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
win_w = 320
win_h = 240

def command(avg_pos):
    if (avg_pos > 10):
        print("Turn Right: Rotate "+str(avg_pos)+" units")
        var = 4
        writeNumber(var)
        print "RPI: Hi Arduino, I sent you", var
    elif (avg_pos < -10):
        print("Turn Left: Rorate "+str(avg_pos)+" units")
        var = 3
        writeNumber(var)
        print "RPI: Hi Arduino, I sent you", var
    else:
        print("Go Straight")
        var = 1
        print "RPI: Hi Arduino, I sent you", var

def mean(l):
    if len(l)==0:
        return 0.0
    return sum(l)/len(l)

def navigate(candidates):
    threading.Timer(0.5, navigate, args=[candidates]).start()
    global command_flag
    global avg_pos
    if candidates:
        avg_pos = mean(candidates)
        command_flag = True
        candidates[:] = []
    else:
        pass

# initialize the nvagation system for different position
global command_flag
global avg_pos
command_flag = False
avg_pos = 0.
candidates = []
navigate(candidates)

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (win_w, win_h)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(win_w, win_h))

# allow the camera to warmup
time.sleep(.1)

init_rawCapture = PiRGBArray(camera, size=(win_w, win_h))

# while(True):
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    flag = False
    img = frame.array
    imshape = img.shape
    vertices = np.array([[(0,imshape[0]),(0,int(imshape[0]/2)), 
        (int(imshape[1]),int(imshape[0]/2)), (imshape[1],imshape[0])]], dtype=np.int32)
    rects, img = detect(img, scale_factor, min_neighs, obj_w, obj_h)
    img = box(rects, img)
    cv2.imshow("Video", img)
    measure(img, rects, candidates)

    if command_flag:
        print("command activated")
        command(avg_pos)
        command_flag = False
        time.sleep(.1)

    rawCapture.truncate(0)
    print('runninng....')
    if(cv2.waitKey(1) & 0xFF == ord('q')):
	   break