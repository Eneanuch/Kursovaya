import asyncio
import logging

import board

import adafruit_dht

from sensors.sensor_head import SensorHead


class DHT22(SensorHead):

    def __init__(self, dht_pin1=board.D23, dht_pin2=board.D24):
        super().__init__()
        self.system_name = 'dht'
        self.devices = [adafruit_dht.DHT22(dht_pin1), adafruit_dht.DHT22(dht_pin2)]

    async def get_data(self, channel: int = 22) -> dict[str: str]:
        # Trying to get data from sensors (throws buffer crowded)
        for i in range(10):
            try:
                data = [(device.temperature, device.humidity) for device in self.devices]
                break
            except Exception as e:
                logging.info(e)
                await asyncio.sleep(1)
        else:
            return {
                'temperature': f"Error",
                'humidity': f"Error"
            }

        # Counting average from all sensors
        temperature = round(sum(map(lambda x: x[0], data)) / len(self.devices), 2)
        humidity = round(sum(map(lambda x: x[1], data)) / len(self.devices), 2)
        print(data)
        return {
            'temperature': f"{temperature}C",
            'humidity': f"{humidity}%"
        }
