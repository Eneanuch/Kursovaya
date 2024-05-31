from web.models import I2CData, SenderData, Statuses
from senders.sender_head import SenderHead
import smbus2


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
        bus = smbus2.SMBus(data.i2cBus)
        byte_value = self.string_to_bytes(data.data)

        chunk_size = 32
        try:
            for i in range(0, len(byte_value), chunk_size):
                chunk = byte_value[i:i + chunk_size]
                bus.write_i2c_block_data(data.i2cAddress, 0x00, chunk)
            return SenderData(status=Statuses.SUCCESS, message=data.data)
        except ValueError as e:
            return SenderData(status=Statuses.FAILURE, message=str(e))
