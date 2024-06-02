import time

from sensors.ACS712 import ACS712
from sensors.DHT22 import DHT22
from sensors.ZMPT101B import ZMPT101B
from sensors.sensor_head import SensorHead

sensors_list: list[SensorHead] = [
    DHT22(),
    ZMPT101B(),
    ACS712()
]

while True:
    for i in sensors_list:
        print(i.get_data())
    time.sleep(2)
