import json
import logging
import os

from logging.config import dictConfig
from fastapi import FastAPI, HTTPException
from starlette.responses import FileResponse, JSONResponse, Response

from models import SendPayload, SMSData, I2CData, UARTData, SenderData
from senders import SenderHead, SmsSender, UARTSender, I2CSender
from sensors import ACS712, DHT22, ZMPT101B, SensorHead

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
    ZMPT101B()
]


#
# To run use in terminal: uvicorn web:app --host 0.0.0.0 --port 80


@app.get('/')
async def index():
    """
    :return: index page
    """
    return FileResponse(root + '/index.html')


@app.get('/get_results')
async def get_results() -> Response:
    """
    get_results() -> Response

    :return: Json results from sensors
    """
    # example data
    data = {
        'humidity': 'Error',
        'temperature': 'Error',
        'current': 'Error',
        'voltage': 'Error',
        'battery': 'Error'
    }
    for sensor in sensors_list:
        data.update(await sensor.get_data())

    return JSONResponse(data)


@app.post("/send_results")
async def send_results(payload: SendPayload) -> Response:
    """
    send_results(payload: SendPayload)

    :param payload: Data from form
    :return: json response with information about successful or failure while sending
    """
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
                f"Отправка данных через I2C по адресу "
                f"{payload.i2cAddress} на шину {payload.i2cBus}."
                f" Данные: {payload.data}")
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

    return JSONResponse(
        {"status": result.status.name, "method": payload.method, "data": result.message}
    )
