# кол-во библиотек в будущем может измениться
import time
import serial
import board
from tkinter import *
from tkinter import ttk
import adafruit_dht
import machine


# from rover_connect import *


class SIM900:
    def __init__(self, port, baudrate, timeout):
        self.mPort = port
        self.mPBaudrate = baudrate
        self.mTimeout = timeout

    def connect(self):
        try:
            self.mConn = serial.Serial(port=self.mPort, baudrate=self.mPBaudrate, timeout=self.mTimeout)
            return True

        except Exception as e:
            print(str(e))
            return False

    def sendMessage(self, phoneNumber, msg):
        try:
            self.mConn.write('AT+CMGF=1\r'.encode())
            time.sleep(0.5)

            cmd = 'AT + CMGS = \"{}\"\r'.format(phoneNumber)
            self.mConn.write(cmd.encode())
            time.sleep(0.5)

            cmd = '{}\r'.format(msg)
            self.mConn.write(cmd.encode())
            time.sleep(0.5)

            self.mConn.write(bytes([2000]))

            time.sleep(0.5)

            return True

        except Exception as e:

            print(str(e))
            return False

    def disconnect(self):
        try:
            self.mConn.close()
            return False

        except Exception as e:
            print(str(e))
            return False


def temperature_and_humidity():
    # получение данных о температуре и влажности c 3-x датчиков

    sensor1 = adafruit_dht.DHT11(board.D4)
    humidity1 = sensor1.humidity
    sensor1.exit()

    sensor2 = adafruit_dht.DHT11(board.D17)
    humidity2 = sensor2.humidity
    sensor2.exit()

    sensor3 = adafruit_dht.DHT11(board.D27)
    humidity3 = sensor3.humidity
    sensor3.exit()

    return [sensor1, humidity1, sensor2, humidity2, sensor3, humidity3]


def battery():
    # получение данных о заряде аккумулятора

    analog_val = machine.ADC(22)
    # led = machine.Pin(25, machine.Pin.OUT)
    # led.low()
    # led.toggle()
    reading = analog_val.read_u16()

    return reading


def power_consumption():
    # общая потребляемая мощность
    # невозможно на данный момент написать код т.к. неизвестен датчик напряжения
    pass


def send():
    # основная функция. получение всех данных и отправка в send()
    temp_and_hum = temperature_and_humidity()

    str = f" temperature 1: {temp_and_hum[0]}\n temperature 2: {temp_and_hum[2]}\n temperature 3: {temp_and_hum[4]}\n humidity 1: {temp_and_hum[1]}\n humidity 2: {temp_and_hum[3]}\n humidity 3: {temp_and_hum[5]}\n humidity 1: {temp_and_hum[1]}\n humidity 2: {temp_and_hum[3]}\n humidity 3: {temp_and_hum[5]}\n battery: {battery()}\n power consumption: {power_consumption()}"

    sim = SIM900("/dev/ttyAMA0", 19200, 1.0)  # example
    sim.connect()

    sim.sendMessage("+1234556667", str)  # example
    sim.disconnect()


if __name__ == "__main__":
    # здесь будет реализована система включения/выключения Raspberry

    root = Tk()
    root.title("Панель управления Raspberry Pi")
    root.geometry("350x100")

    # btn1 = ttk.Button(text="Включение ПК", command=turn_on)
    # btn1.pack()
    # btn2 = ttk.Button(text="Выключение ПК", command=turn_off)
    # btn2.pack()
    btn3 = ttk.Button(text="Отправка СМС", command=send)
    btn3.pack()

    root.mainloop()
