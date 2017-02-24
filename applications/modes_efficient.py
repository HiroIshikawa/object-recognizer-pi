import time
import g
from measure import * 
from interface import *
from detect import *
#def auto(stop_event):
#    g.track_flag
#    check_candidates(stop_event)
#    while(not stop_event.is_set()):
#        if g.track_flag:
#            track(g.avg_pos)
#            g.track_flag = False
#            time.sleep(.1)

def auto(camera,rawCapture,cas_params,stop_event):
    print("In Auto Detction System for PiCamera...")
    g.track_flag
    check_candidates(stop_event)
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        flag = False
        raw_img = frame.array
        # cv2.imshow("Raw", img)
        # img = preprocess(img)
        # cv2.imshow("Preprocessed", img)
        rects, detected_img = detect(raw_img, cas_params)
        g.img = box(rects, detected_img)
    #    cv2.imshow("Cascaded", img)
        measure(raw_img, rects)

        # if there's no rects found, look around
        # if not rects:
        #     look_around() 
            # Check time elapsed, if over 10 sec, invoke spiral search
            # if (time.time()-start) > 10:
            #     spiral_search()
        if g.track_flag:
            track(g.avg_pos)
            g.track_flag = False
            #time.sleep(.1)
        rawCapture.truncate(0)

def manual():
    print("Entering manual mode, stop current movement")
    writeNumber(0)
    while True:

        w = 1
        s = 0
        x = 2
        a = 3
        d = 4
        q = 5
        e = 6

        var = raw_input("Enter command: ")
        print('Your input: '+str(var))
        # writeNumber(int(var))
        if var=='m':
            print("Entering manual mode, stop current movement")
            writeNumber(0)
            break
        writeNumber(int(var))
        print "RPI: Hi Arduino, I sent you", var
