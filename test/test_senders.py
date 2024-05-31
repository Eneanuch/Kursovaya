import smbus2
import time

from ..models import I2CData
from ..senders import I2CSender

bus = smbus2.SMBus(1)
address = 0x04

test_data = {
        'humidity': 'Error',
        'temperature': 'Error',
        'current': 'Error',
        'voltage': 'Error',
        'battery': 'Error'
    }
data = I2CData(
    i2cAddress=0x04,
    i2cBus=1,
    data=str(test_data)
)
i2c_sender = I2CSender()
i2c_sender.send_data(data)