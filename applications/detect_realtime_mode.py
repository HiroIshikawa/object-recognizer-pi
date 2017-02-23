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


def mean(l):
    if len(l)==0:
        return 0.0
    return sum(l)/len(l)

def navigate(stop_event):
    global candidates
    t = threading.Timer(0.5, navigate, args=[stop_event])
    t.start()
    if stop_event.is_set():
        t.cancel()
    global track_flag
    global avg_pos
    if candidates:
        avg_pos = mean(candidates)
        track_flag = True
        candidates[:] = []
    else:
        pass

def manual():
    print("Entering manual mode, stop current movement")
    # writeNumber(0)
    while True:

        w = 1
        s = 0
        x = 2
        a = 3
        d = 4
        q = 5
        e = 6

        var = raw_input("Enter command: ")
        # writeNumber(var)
        if var=='m':
            print("Entering manual mode, stop current movement")
            # writeNumber(0)
            break

        print "RPI: Hi Arduino, I sent you", var

def detection_system(cap,cas_params):
    global img
    global track_flag
    global avg_pos
    global candidates
    # track_flag = False
    avg_pos = 0.
    print("In auto..")
    # navigate(stop_event)
    while(True):
        ret, raw_img = cap.read()
        imshape = raw_img.shape
        vertices = np.array([[(0,imshape[0]),(0,int(imshape[0]/2)), 
            (int(imshape[1]),int(imshape[0]/2)), (imshape[1],imshape[0])]], dtype=np.int32)
        # cv2.imshow("Raw", img)
        processed_img = region_of_interest(raw_img, vertices)
        # cv2.imshow("Preprocessed", img)
        rects, detected_img = detect(processed_img, cas_params)
        img = box(rects, detected_img)
        measure(img, rects, candidates)

def auto(stop_event):
    global track_flag
    track_flag = False
    global avg_pos
    global candidates
    navigate(stop_event)
    while(not stop_event.is_set()):
        if track_flag:
            track(avg_pos)
            track_flag = False
            time.sleep(.1)

def mode_controller(power, cap, cas_params):
    while (True):
        input = raw_input("Manual (m) or Auto (a)?: ")
        if input == 'm':
            print('Activating manual mode..')
            manual()
        elif input == 'a':
            print('Activating auto mode..')
            auto_thread_stop = threading.Event()
            auto_thread = threading.Thread(target=auto, args=[auto_thread_stop])
            auto_thread.daemon = True
            auto_thread.start()
            input = raw_input("Mode Change Accepting...")
            if input:
                auto_thread_stop.set()
                print("Object Tracker Stopped.")
                pass
        elif input == 'q':
            print('Deactivating..')
            power = 'off'
        else:
            pass

scale_factor = float(argv[1])
min_neighs = int(argv[2])
obj_w = int(argv[3])
obj_h = int(argv[4])
win_w = int(argv[5])
win_h = int(argv[6])

# pack parms for cascades
cas_params = (scale_factor, min_neighs, obj_w, obj_h)

# global cap
cap = cv2.VideoCapture(0)
cap.set(3,win_w)
cap.set(4,win_h)
time.sleep(.1)

# global img
global img
ret, img = cap.read()

# power
power = 'on'


global candidates
candidates = []
detection_thread = threading.Thread(target=detection_system, args=[cap, cas_params])
detection_thread.daemon = True
detection_thread.start()
print("Detection System Initiated.")

# now threading1 runs regardless of user input
controller_thread = threading.Thread(target=mode_controller, args=[power,cap,cas_params])
controller_thread.daemon = True
controller_thread.start()
print("Control System Initiated.")

while(power):
    if img.any():
        window_name="Cascaded"
        cv2.namedWindow(window_name)
        cv2.imshow(window_name, img)
        cv2.waitKey(1)
    if power=='off':
        "Powering off..."
        break
