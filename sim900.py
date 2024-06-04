import serial
import RPi.GPIO as GPIO
import os
import time

GPIO.setmode(GPIO.BOARD)

# Enable Serial Communication
ser = serial.Serial("/dev/serial0", baudrate=9600, timeout=1)

def send_command(command, wait_for_response=True):
    ser.write((command + '\r').encode())
    time.sleep(1)  # Небольшая задержка для обработки команды

    if wait_for_response:
        response = ser.read_all().decode()
        return response
    return None

# Пример использования
def main():
    response = send_command('AT')
    print('Response:', response)

    response = send_command('AT+CSQ')
    print('Signal Quality:', response)

    while True:
        line = ser.readline().decode().strip()
        if line:
            print('Received:', line)
            if 'BU,DNHG>2' in line:
                print('Special message received:', line)
                # Выполнить нужные действия при получении этого сообщения

if __name__ == '__main__':
    main()