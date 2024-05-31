import smbus2
import time

bus = smbus2.SMBus(1)
address = 0x04

def writeData(value):
    byteValue = StringToBytes(value)
    bus.write_i2c_block_data(address,0x00,byteValue) #first byte is 0=command byte.. just is.
    return -1


def StringToBytes(val):
        retVal = []
        for c in val:
            retVal.append(ord(c))
        return retVal

while True:
    print("sending")
    writeData("test")
    time.sleep(5)

    print('OPEN')
    writeData("OPEN-00-00")
    time.sleep(7)

    print('WIN')
    writeData("WIN-12-200")
    time.sleep(7)