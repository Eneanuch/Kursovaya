import serial
import time

# Set up the serial connection to the Arduino
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

# Give some time for the connection to establish
time.sleep(2)

# Function to send data to Arduino
def send_data(data):
    arduino.write((data + '\n').encode())

# Example of sending data
try:
    while True:
        send_data("Hello, Arduino!")
        time.sleep(1)
except KeyboardInterrupt:
    print("Communication stopped")
finally:
    arduino.close()
