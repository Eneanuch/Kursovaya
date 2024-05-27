import board

import adafruit_dht

from sensors.sensor_head import SensorHead


class DHT22(SensorHead):

    def __init__(self, dht_pin1=board.D16, dht_pin2=board.D18):
        super().__init__()
        self.system_name = 'dht'
        self.devices = [adafruit_dht.DHT22(dht_pin1), adafruit_dht.DHT22(dht_pin2)]

    def get_data(self, channel: int = 22) -> dict[str: str]:
        # Считает среднее с трех датчиков
        data = [(device.temperature, device.humidity) for device in self.devices]

        temperature = round(sum(map(lambda x: x[1], data)) / 3, 2)
        humidity = round(sum(map(lambda x: x[0], data)) / 3, 2)

        return {
            'temperature': f"{temperature}*C",
            'humidity': f"{humidity}%"
        }
