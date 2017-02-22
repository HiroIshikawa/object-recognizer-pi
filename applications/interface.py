import smbus
# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(1)
address = 0x04

def writeNumber(value):
    try:
        bus.write_byte(address, value)
    except IOError:
        print('IOError happend')
        pass
#    # bus.write_byte_data(address, 0, value)

def readNumber():
    number = bus.read_byte(address)
    # number = bus.read_byte_data(address, 1)
    return number

# def command(avg_pos):
#     if (avg_pos > 10):
#         print("Turn Right: Rotate "+str(avg_pos)+" units")
#         var = 4
#         writeNumber(var)
#         print "RPI: Hi Arduino, I sent you", var
#     elif (avg_pos < -10):
#         print("Turn Left: Rorate "+str(avg_pos)+" units")
#         var = 3
#         writeNumber(var)
#         print "RPI: Hi Arduino, I sent you", var
#     else:
#         print("Go Straight")
#         var = 1
#         print "RPI: Hi Arduino, I sent you", var

def track(avg_pos):
    if (avg_pos > 10):
        print("Turn Right: Rotate "+str(avg_pos)+" units")
        var = 4
        writeNumber(var)
        print "RPI: Hi Arduino, I sent you", var
        # time.sleep(.5)
        # writeNumber(0)
    elif (avg_pos < -10):
        print("Turn Left: Rorate "+str(avg_pos)+" units")
        var = 3
        writeNumber(var)
        print "RPI: Hi Arduino, I sent you", var
        # time.sleep(.5)
        # writeNumber(0)
    else:
        print("Go Straight")
        var = 1
        print "RPI: Hi Arduino, I sent you", var
        # time.sleep(5)
        # writeNumber(0)

# def look_around():
#     # direction : right / left
#     # unit : time duration
#     # writeNumber(4) # turn right
#     # time.sleep(.3)
#     # writeNumber(0)
#     return

# def spiral_search():
#     return