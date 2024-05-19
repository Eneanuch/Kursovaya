import time

import serial

from senders.sender_head import SenderHead


class SmsSender(SenderHead):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.serial = serial.Serial(
            port=kwargs.get('port', '/dev/ttyS0'),
            baudrate=kwargs.get('baudrate', 9600),
            timeout=kwargs.get('timeout', 1)
        )
        self.setup_gsm()

    def send_at_command(self, command, expected_response, timeout=2):
        self.serial.write((command + '\r').encode())
        time.sleep(0.5)
        end_time = time.time() + timeout
        while time.time() < end_time:
            if self.serial.in_waiting > 0:
                response = self.serial.read(self.serial.in_waiting).decode()
                if expected_response in response:
                    return response
        return None

    def setup_gsm(self) -> bool:
        if self.send_at_command('AT', 'OK') is None:
            return False

        if self.send_at_command('AT+CMGF=1', 'OK') is None:
            return False
        return True

    def send_data(self, *args, **data) -> bool:
        if self.send_at_command(f'AT+CMGS="{data["phonenumber"]}"', '>') is not None:
            self.serial.write((data["message"] + '\x1A').encode())
            if self.send_at_command('', 'OK', timeout=10) is not None:
                return True
            else:
                return False
        return False
