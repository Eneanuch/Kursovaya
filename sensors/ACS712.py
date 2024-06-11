import logging

import board
import busio

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

from sensors.sensor_head import SensorHead


class ACS712(SensorHead):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.system_name = 'ACS712'
        try:
            i2c = busio.I2C(board.SCL, board.SDA)
            self.ads = ADS.ADS1115(i2c)
            self.chan = AnalogIn(self.ads, ADS.P1)
        except ValueError as e:
            logging.error(f"ACS712 sensor not connected ({ADS.P1})")

    async def get_data(self, *args, **kwargs) -> dict[str: str]:
        voltage = self.chan.voltage
        current = round((voltage - 2.5) / 0.185, 2)  # config for 5A
        return {
            "current": f"{current}A"
        }
