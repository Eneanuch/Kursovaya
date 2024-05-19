from senders.sender_head import SenderHead
import smbus

class I2CSender(SenderHead):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def send_data(self, **data) -> bool:
        bus = smbus.SMBus(data.get('bus', 1))
        byte_data = data.get('message').encode('utf-8')
        bus.write_i2c_block_data(data.get('i2c_address'), data.get('offset', 0), list(byte_data))
        return True