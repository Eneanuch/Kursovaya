from enum import Enum
from typing import Union

from pydantic import BaseModel


class Statuses(Enum):
    SUCCESS = 0
    FAILURE = -1


class SenderData(BaseModel):
    status: Statuses
    message: str = 'OK'


class BoardData(BaseModel):
    humidity: str
    temperature: str
    amperage: str
    battery: str


class SMSData(BaseModel):
    phoneNumber: str
    data: str


class I2CData(BaseModel):
    i2cAddress: str
    i2cBus: int
    data: str


class UARTData(BaseModel):
    uartPort: str
    baudRate: int
    timeout: int
    data: str


class SendPayload(BaseModel):
    method: str
    data: Union[BoardData, str]
    phoneNumber: Union[str, None] = None
    i2cAddress: Union[str, None] = None
    i2cBus: Union[int, None] = None
    uartPort: Union[str, None] = None
    baudRate: Union[int, None] = None
    timeout: Union[int, None] = None
