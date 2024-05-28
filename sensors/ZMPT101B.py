import board
import busio

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

from sensors.sensor_head import SensorHead


class ZMPT101B(SensorHead):

    MAX_BATTERY_LEVEL = 5.2
    MIN_BATTERY_LEVEL = 3.4

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.system_name = 'ZMPT101B'
        i2c = busio.I2C(board.SCL, board.SDA)
        self.ads = ADS.ADS1115(i2c)
        self.chan = AnalogIn(self.ads, ADS.P0)

    def get_battery_level(self, voltage) -> float:
        if voltage >= self.MAX_BATTERY_LEVEL:
            return 100
        elif voltage <= self.MIN_BATTERY_LEVEL:
            return 0
        voltage -= self.MIN_BATTERY_LEVEL
        return round(voltage / (self.MAX_BATTERY_LEVEL - self.MIN_BATTERY_LEVEL), 2)

    def get_data(self, *args, **kwargs) -> dict[str: str]:
        voltage = round(self.chan.voltage, 2)

        return {
            "battery": f"{self.get_battery_level(voltage)}%",
            "voltage": f"{voltage}V"
        }
