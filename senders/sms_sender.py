import logging
import time

import serial

from models import SMSData, SenderData, Statuses
from senders.sender_head import SenderHead


class SmsSender(SenderHead):
    def __init__(self, *args, port='/dev/serial0', baudrate=9600, timeout=1, **kwargs):
        super().__init__(*args, **kwargs)

        self.serial = serial.Serial(
            port=port,
            baudrate=baudrate,
            timeout=timeout
        )
        if not self.setup_gsm():
            logging.error("GSM не получается подключить")

    def send_at_command(self, command: str, expected_response: str, timeout: int = 2):
        """
        Send command by serial port to device

        :param command: text of command
        :param expected_response: what you need in response
        :param timeout: how much time give to the device to answer
        :return: response or None
        """

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
        """
        Setup GSM device

        :return: True if GSM device is OK else False
        """
        if self.send_at_command('AT', 'OK') is None:
            return False

        if self.send_at_command('AT+CMGF=1', 'OK') is None:
            return False
        return True

    def send_data(self, data: SMSData) -> SenderData:
        if self.send_at_command(f'AT+CMGS="{data.phoneNumber}"', '>') is not None:
            self.serial.write((data.data + '\x1A').encode())
            if self.send_at_command('', 'OK', timeout=10) is not None:
                return SenderData(status=Statuses.SUCCESS, message='OK')
            else:
                return SenderData(status=Statuses.FAILURE, message='GSM не отвечает после отправки сообщения')
        return SenderData(status=Statuses.FAILURE, message='GSM не отвечает при попытке отправить сообщение')
