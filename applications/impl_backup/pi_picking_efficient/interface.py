import time

try:
    import smbus
    bus = smbus.SMBus(1)
    address = 0x04
except ImportError:
    print('Not importing smbus')
    pass
# for RPI version 1, use "bus = smbus.SMBus(0)"

def writeNumber(value):
    try:
        bus.write_byte(address, value)
    except IOError:
        # print('IOError happend')
        pass
    except NameError:
        # print('NameError happend')
        # print('You may run this program not on Pi')
        pass
#    # bus.write_byte_data(address, 0, value)

def readNumber():
    try:
        number = bus.read_byte(address)
    except IOError:
        number = -1
        pass
    # number = bus.read_byte_data(address, 1)
    except NameError:
        number = -1
        pass
    return number

# def look_around():
#     # direction : right / left
#     # unit : time duration
#     # writeNumber(4) # turn right
#     # time.sleep(.3)
#     # writeNumber(0)
#     return

# def spiral_search():
#     return

def track(avg_pos):
    if avg_pos > 300:
        print("Detected at +"+str(avg_pos)+" units, Rotate Right.")
        var = 4  # rotate right
        writeNumber(var)
    elif avg_pos < -300:
        print("Detected at "+str(avg_pos)+" units, : Rotate Left.")
        var = 3  # rotate left
        writeNumber(var)
    elif avg_pos > 40:
        print("Detected at +"+str(avg_pos)+" units, Tilt Right.")
        var = 7  # tilt right
        writeNumber(var)
    elif avg_pos < -40:
        print("Detected at "+str(avg_pos)+" units, Tilt Left.")
        var = 6  # tilt left
        writeNumber(var)
    else:
        print("Detected at "+str(avg_pos)+" units, Go Straight: ")
        var = 1  # go straight
        writeNumber(var)

def monitor(avg_pos):
    if avg_pos < 150 or avg_pos > -150:
        distance = readNumber()
        # print('Appx distance to the object: '+str(distance))
    else:
        distance = -1
    print('Distance reading: '+str(distance))
    if distance > 0 and distance < 15 and not distance == 1:
        accm_time = time.time()
        start_time = time.time()
        # pickup()  # picking up mode initiation
        # writeNumber(0)
        writeNumber(8)
        while True:
            if time.time()-start_time > 1.:  # 
                complete = readNumber()
                print('Complete?: '+str(complete))
                if complete==1:
                    print('Received Complete Signal From Arduino')
                    writeNumber(0)
                    time.sleep(5)
                    break
                start_time = time.time()
            if time.time()-accm_time > 10.:  # if 10 seconds passed after initiating picking up sequence
                print('10 seconds passed. Backing detection state.')
                writeNumber(0)
                time.sleep(5)
                break
