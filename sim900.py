import serial
import RPi.GPIO as GPIO
import os
import time

GPIO.setmode(GPIO.BOARD)

# Enable Serial Communication
port = serial.Serial("/dev/serial0", baudrate=9600, timeout=1)

# Transmitting AT Commands to the Modem
# '\r\n' indicates the Enter key

port.write(('AT' + '\r\n').encode())
rcv = port.read(10)
print(rcv)
time.sleep(1)

port.write(('ATE0' + '\r\n').encode())  # Disable the Echo
rcv = port.read(10)
print(rcv)
time.sleep(1)

port.write(('AT+CMGF=1' + '\r\n').encode())  # Select Message format as Text mode
rcv = port.read(10)
print(rcv)

time.sleep(1)

port.write(('AT+CNMI=2,1,0,0,0' + '\r\n').encode())  # New SMS Message Indications
rcv = port.read(10)
print(rcv)

time.sleep(1)

# Sending a message to a particular Number

port.write(('AT+CMGS="XXXXXXXXXX"' + '\r\n').encode())
rcv = port.read(10)
print(rcv)

time.sleep(1)

port.write(('Hello User' + '\r\n').encode())  # Message
rcv = port.read(10)
print(rcv)


port.write(("\x1A").encode())  # Enable to send SMS
for i in range(10):
    rcv = port.read(10)
    print(rcv)
