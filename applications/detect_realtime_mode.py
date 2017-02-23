from sys import argv
import sys
import cv2
import numpy as np
import time
import threading

import g
from controller import *
from modes import *
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

# Setting up camera
cap = cv2.VideoCapture(0)
cap.set(3,win_w)
cap.set(4,win_h)
time.sleep(.1)

# Pack parms for cascades
cas_params = (scale_factor, min_neighs, obj_w, obj_h)

# Image file used accross threads
ret, g.img = cap.read()

# Initiate a thread for detection system
detection_thread = threading.Thread(target=detection_system, args=[cap, cas_params])
detection_thread.daemon = True
detection_thread.start()

# Initiate a therad for control system
controller_thread = threading.Thread(target=mode_controller, args=[cap,cas_params])
controller_thread.daemon = True
controller_thread.start()

# Main thread, exit when user send quit command in control system prompt
# while(power):
while(g.power):
    # if img.any():
    if g.img.any():
        window_name="Cascaded"
        cv2.namedWindow(window_name)
        # cv2.imshow(window_name, img)
        cv2.imshow(window_name, g.img)
        cv2.waitKey(1)
    # if power=='off':
    if g.power=='off':
        break
