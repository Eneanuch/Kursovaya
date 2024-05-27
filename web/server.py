import json
import logging
import os
from logging.config import dictConfig

from fastapi import FastAPI, HTTPException
from starlette.responses import FileResponse, JSONResponse

from models import SendPayload, SMSData, I2CData, UARTData, SenderData
from senders.i2c_sender import I2CSender
from senders.sender_head import SenderHead
from senders.sms_sender import SmsSender
from senders.uart_sender import UARTSender
from sensors.ACS712 import ACS712
from sensors.DHT22 import DHT22
from sensors.ZMPT101B import ZMPT101B
from sensors.sensor_head import SensorHead

app = FastAPI()
root = os.path.dirname(os.path.abspath(__file__))

with open('logging_config.json', 'r') as f:
    logging_config = json.load(f)
    dictConfig(logging_config)

logger = logging.getLogger(__name__)

senders_dict: dict[str, SenderHead] = {
    "sms": SmsSender(),
    "uart": UARTSender(),
    "i2c": I2CSender()
}

sensors_list: list[SensorHead] = [
    ACS712(),
    DHT22(),
    ZMPT101B(),
]

# run with uvicorn web:app --host 0.0.0.0 --port 80


@app.get('/')
async def results():
    return FileResponse(root + '/index.html')


@app.get('/get_results')
async def get_results():
    # example data
    data = {
        'humidity': '45%',
        'temperature': '22°C',
        'current': '3.5A',
        'voltage': '5V',
        'battery': '75%'
    }
    for sensor in sensors_list:
        data.update(sensor.get_data())

    return JSONResponse(data)


@app.post("/send_results")
async def send_results(payload: SendPayload):
    match payload.method:
        case "sms":
            if payload.phoneNumber is None:
                raise HTTPException(status_code=400, detail="Нужен телефон для отправки сообщения")
            logger.info(f"Отправка SMS по номеру {payload.phoneNumber}. Данные: {payload.data}")
            data = SMSData(
                phoneNumber=payload.phoneNumber,
                data=payload.data
            )
        case "i2c":
            if payload.i2cAddress is None or payload.i2cBus is None:
                raise HTTPException(status_code=400, detail="I2C адрес и шина нужны для отправки данных")
            logger.info(
                f"Отправка данных через I2C по адресу {payload.i2cAddress} на шину {payload.i2cBus}. Данные: {payload.data}")
            data = I2CData(
                i2cAddress=payload.i2cAddress,
                i2cBus=payload.i2cBus,
                data=payload.data,
            )
        case "uart":
            if payload.uartPort is None or payload.baudRate is None or payload.timeout is None:
                raise HTTPException(status_code=400,
                                    detail="UART порт, скорость, таймаут нужны для отправки данных по UART")
            logger.info(
                f"Отправка данных по UART по порту {payload.uartPort} со скоростью {payload.baudRate} и таймаутом {payload.timeout}. Данные: {payload.data}")

            data = UARTData(
                port=payload.uartPort,
                baudRate=payload.baudRate,
                timeout=payload.timeout,
                data=payload.data
            )
        case _:
            raise HTTPException(status_code=400, detail="Неверный метод")

    result: SenderData = senders_dict[payload.method].send_data(data)

    return {"status": result.status.name, "method": payload.method, "data": result.message}
