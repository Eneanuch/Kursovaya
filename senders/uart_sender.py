import serial

from senders.sender_head import SenderHead


class UARTSender(SenderHead):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def send_data(self, **data) -> bool:
        self.serial = serial.Serial(
            data.get('port', '/dev/serial0'),
            data.get('badurate', 9600),
            timeout=data.get('timeout', 1),
        )
        self.serial.write((data.get('message') + '\n').encode(data.get('encoding', 'utf-8')))
