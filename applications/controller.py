import threading
import g
from modes import *

def mode_controller():
    while (True):
        input = raw_input("Manual (m), Auto (a), or Quit (q)?: ")
        if input == 'm':
            print('Activating manual mode...')
            manual()
        elif input == 'a':
            print('Activating auto mode...')
            auto_thread_stop = threading.Event()
            auto_thread = threading.Thread(target=auto, args=[auto_thread_stop])
            auto_thread.daemon = True
            auto_thread.start()
            input = raw_input("Mode Change Accepting (m)...")
            if input:
                auto_thread_stop.set()
                print("Object Tracker Stopped.")
                pass
        elif input == 'q':
            print('Powering Off...')
            g.power = 'off'
        else:
            pass

