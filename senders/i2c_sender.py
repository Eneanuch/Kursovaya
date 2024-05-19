from models import I2CData, SenderData, Statuses
from senders.sender_head import SenderHead
import smbus


class I2CSender(SenderHead):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def send_data(self, data: I2CData) -> SenderData:
        bus = smbus.SMBus(data.i2cBus)
        byte_data = data.data.encode('utf-8')
        bus.write_i2c_block_data(data.i2cAddress, 0, list(byte_data))
        return SenderData(status=Statuses.SUCCESS, message=byte_data)
