from models import I2CData, SenderData, Statuses
from senders.sender_head import SenderHead
import smbus


class I2CSender(SenderHead):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @staticmethod
    def string_to_bytes(data: str):
        byte_value = []
        for c in data:
            byte_value.append(ord(c))
        return byte_value

    def send_data(self, data: I2CData) -> SenderData:
        bus = smbus.SMBus(data.i2cBus)
        byte_value = self.string_to_bytes(data.data)
        bus.write_i2c_block_data(data.i2cAddress, 0x00, byte_value)
        return SenderData(status=Statuses.SUCCESS, message=data.data)
