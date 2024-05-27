from sensors.DHT22 import DHT22
from sensors.sensor_head import SensorHead

sensors_list: list[SensorHead] = [
    DHT22(),
]

while True:
    for i in sensors_list:
        print(i.get_data())

