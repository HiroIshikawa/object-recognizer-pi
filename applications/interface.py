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