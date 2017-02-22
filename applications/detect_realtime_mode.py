from detect import *
# from interface import *
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

global obj_w
global obj_h
global scale_factor
global min_neighs
global win_w
global win_h

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

def navigate(candidates, stop_event):
    t = threading.Timer(0.5, navigate, args=[candidates,stop_event])
    t.start()
    if stop_event.is_set():
        t.cancel()
    global command_flag
    global avg_pos
    if candidates:
        avg_pos = mean(candidates)
        command_flag = True
        candidates[:] = []
    else:
        pass

def manual():
    print("in manual mode")
    while True:

        w = 1
        s = 0
        x = 2
        a = 3
        d = 4
        q = 5
        e = 6

        var = raw_input("Enter Command: ")
        if var=='m':
            break
    #    if not  var:
    #        continue

        # writeNumber(var)
        print "RPI: Hi Arduino, I sent you", var
        # sleep one second
        # time.sleep(1)

        # number = readNumber()
        # print "Arduino: Hey RPI, I received a digit", number
        # print

def auto(stop_event):
    global obj_w
    global obj_h
    global scale_factor
    global min_neighs
    global win_w
    global win_h

    global img

    global cap
    global command_flag
    global avg_pos
    command_flag = False
    avg_pos = 0.
    candidates = []
    navigate(candidates, stop_event)
    print("In auto..")
    while(not stop_event.is_set()):
        flag = False
        ret, img = cap.read()
        imshape = img.shape
        vertices = np.array([[(0,imshape[0]),(0,int(imshape[0]/2)), 
            (int(imshape[1]),int(imshape[0]/2)), (imshape[1],imshape[0])]], dtype=np.int32)
        # cv2.imshow("Raw", img)
        img = region_of_interest(img, vertices)
        # cv2.imshow("Preprocessed", img)
        rects, img = detect(img, scale_factor, min_neighs, obj_w, obj_h)
        img = box(rects, img)
        measure(img, rects, candidates)
        if command_flag:
            print("command activated")
            command(avg_pos)
            command_flag = False
            time.sleep(.1)
        # if(cv2.waitKey(1) & 0xFF == ord('q')):
        #     break
        # cv2.waitKey(1)
        # cv2.waitKey(1)
        # cv2.destroyAllWindows()

def mode_controller():
    global switch
    # switch = 'on'
    while (True):
        input = raw_input("Manual (m) or Auto (a)?: ")
        if input == 'm':
            print('Activating manual mode..')
            manual()
        elif input == 'a':
            print('Activating auto mode..')
            t2_stop= threading.Event()
            threading2 = threading.Thread(target=auto,args=[t2_stop])
            threading2.daemon = True
            threading2.start()
            # auto()
            input = raw_input("Switch back?: ")
            if input:
                t2_stop.set()
                pass
        elif input == 'q':
            print('Deactivating..')
            switch = 'off'
        else:
            pass

global cap
cap = cv2.VideoCapture(0)
cap.set(3,win_w)
cap.set(4,win_h)
time.sleep(.1)
print('Camera activated')

global img
ret, img = cap.read()

# now threading1 runs regardless of user input
threading1 = threading.Thread(target=mode_controller)
threading1.daemon = True
threading1.start()

global switch
switch = 'on'

while(switch):
    if img.any():
        window_name="Cascaded"
        cv2.namedWindow(window_name)
        cv2.imshow(window_name, img)
        cv2.waitKey(1)
    if switch=='off':
        break


# while(True):
#     input = raw_input("Manual (m) or Auto (a)?: ")
#     if input == 'm':
#         print('Activating manual mode..')
#         manual()
#     elif input == 'a':
#         print('Activating auto mode..')
#         auto()
#     else:
#         pass