import serial

from models import SenderData, UARTData, Statuses
from senders.sender_head import SenderHead


class UARTSender(SenderHead):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def send_data(self, data: UARTData) -> SenderData:
        self.serial = serial.Serial(
            data.uartPort,
            data.baudRate,
            timeout=data.timeout,
        )
        self.serial.write((data.data + '\n').encode('utf-8'))

        return SenderData(status=Statuses.SUCCESS, message='OK')
