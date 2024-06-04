import serial
import time

arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

time.sleep(2)


def send_data(data):
    arduino.write((data + '\n').encode())


try:
    while True:
        send_data("ON")
        print("Sent: ON")
        time.sleep(5)

        send_data("OFF")
        print("Sent: OFF")
        time.sleep(5)
except KeyboardInterrupt:
    print("Communication stopped")
finally:
    arduino.close()
