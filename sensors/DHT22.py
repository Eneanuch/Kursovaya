import Adafruit_DHT as dht

from sensors.sensor_head import SensorHead


class DHT22(SensorHead):

    def __init__(self, dht_pin1=22, dht_pin2=16, dht_pin3=18):
        super().__init__()
        self.system_name = 'dht'
        self.pins = [dht_pin1, dht_pin2, dht_pin3]

    def get_data(self, channel: int = 22) -> dict[str: str]:
        # Считает среднее с трех датчиков
        data = [dht.read_retry(dht.DHT22, i) for i in self.pins]

        temperature = round(sum(map(lambda x: x[1], data)) / 3, 2)
        humidity = round(sum(map(lambda x: x[0], data)) / 3, 2)

        return {
            'temperature': f"{temperature}*C",
            'humidity': f"{humidity}%"
        }
