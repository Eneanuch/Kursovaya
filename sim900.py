import serial
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

ser = serial.Serial("/dev/serial0", baudrate=9600, timeout=1)


def send_command(command, wait_for_response=True):
    ser.write((command + '\r').encode())
    time.sleep(1)

    if wait_for_response:
        response = ser.read_all().decode()
        return response
    return None


def send_sms(phone_number, message):
    time.sleep(1)

    send_command('AT+CMGF=1')

    send_command('AT+CMGS="{}"'.format(phone_number))
    send_command(message, wait_for_response=False)
    ser.write(bytes([26]))
    time.sleep(1)

    response = ser.read_all().decode()
    print(response)


def main():
    response = send_command('AT')
    print('Response:', response)

    response = send_command('AT+CSQ')
    print('Signal Quality:', response)

    send_sms("79807998558", "Hello World")
    time.sleep(10)

    # while True:
    #     line = ser.readline().decode().strip()
    #     if line:
    #         print('Received:', line)
    #         time.sleep(1)


if __name__ == '__main__':
    main()