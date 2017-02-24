import time
import g
from measure import * 
from interface import *

def auto(stop_event):
    g.track_flag
    check_candidates(stop_event)
    while(not stop_event.is_set()):
        if g.track_flag:
            track(g.avg_pos)
            g.track_flag = False
            time.sleep(.1)

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
