
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
        print('IOError happend')
        pass
    except NameError:
        # print('NameError happend')
        # print('You may run this program not on Pi')
        pass
#    # bus.write_byte_data(address, 0, value)

def readNumber():
    number = bus.read_byte(address)
    # number = bus.read_byte_data(address, 1)
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
    if (avg_pos > 300):
        print("Detected at +"+str(avg_pos)+" units, Rotate Right.")
        var = 4  # rotate right
        writeNumber(var)
    elif (avg_pos < -300):
        print("Detected at "+str(avg_pos)+" units, : Rotate Left.")
        var = 3  # rotate left
        writeNumber(var)
    elif (avg_pos > 40):
        print("Detected at +"+str(avg_pos)+" units, Tilt Right.")
        var = 7  # tilt right
        writeNumber(var)
    elif (avg_pos < -40):
        print("Detected at "+str(avg_pos)+" units, Tilt Left.")
        var = 6  # tilt left
        writeNumber(var)
    else:
        print("Detected at "+str(avg_pos)+" units, Go Straight: ")
        var = 1  # go straight
        writeNumber(var)
