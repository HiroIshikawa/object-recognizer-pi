from sys import argv
import sys
import cv2
import numpy as np
import time
import threading

from picamera.array import PiRGBArray
from picamera import PiCamera

import g
from controller_efficient import *
from modes_efficient import *
from preprocess import *
from detect import *
from measure import *
from interface import *

# Params for camera and object detection
scale_factor = float(argv[1])
min_neighs = int(argv[2])
obj_w = int(argv[3])
obj_h = int(argv[4])
win_w = int(argv[5])
win_h = int(argv[6])

# make params pack for cascade
cas_params = (scale_factor, min_neighs, obj_w, obj_h)

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (win_w, win_h)
camera.framerate = 64
rawCapture = PiRGBArray(camera, size=(win_w, win_h))
time.sleep(.1) # allow the camera to warmup
# init_rawCapture = PiRGBArray(camera, size=(win_w, win_h))

# Image file used across threads
camera.capture(rawCapture, 'bgr')
g.img = rawCapture.array
rawCapture.truncate(0)
 
# Initiate a thread for PiCamera detection system
# detection_thread = threading.Thread(target=pi_detection_system, args=[camera, rawCapture, cas_params])
# detection_thread.daemon = True
# detection_thread.start()

# Initiate a therad for control system
controller_thread = threading.Thread(target=mode_controller,args=[camera,rawCapture,cas_params])
controller_thread.daemon = True
controller_thread.start()

# Main thread, exit when user send quit command in control system prompt
while(g.power):
    if g.img.any():
        #window_name="Cascaded"
        # cv2.namedWindow(window_name)
        #cv2.imshow(window_name, g.img)
        #cv2.waitKey(1)
        pass
    if g.power=='off':
        break
