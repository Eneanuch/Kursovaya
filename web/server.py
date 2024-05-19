import os

from fastapi import FastAPI, HTTPException
from starlette.responses import FileResponse, JSONResponse

from models import SendPayload

app = FastAPI()
root = os.path.dirname(os.path.abspath(__file__))

# run with uvicorn web:app --host 0.0.0.0 --port 80

senders_classes = [

]

@app.get('/')
async def results():
    return FileResponse('index.html')


@app.get('/get_results')
async def get_results():
    # example data
    data = {
        'humidity': '45%',
        'temperature': '22°C',
        'amperage': '3.5A',
        'battery': '75%'
    }
    return JSONResponse(data)


@app.post("/send_results")
async def send_results(payload: SendPayload):
    match payload.method:
        case "sms":
            if payload.phoneNumber is None:
                raise HTTPException(status_code=400, detail="Нужен телефон для отправки сообщения")
            print(f"Отправка SMS по номеру {payload.phoneNumber}. Данные: {payload.data}")

        case "i2c":
            if payload.i2cAddress is None or payload.i2cBus is None:
                raise HTTPException(status_code=400, detail="I2C адрес и шина нужны для отправки данных")
            print(f"Отправка данных через I2C по адресу {payload.i2cAddress} на шину {payload.i2cBus}. Данные: {payload.data}")

        case "uart":
            if payload.uartPort is None or payload.baudRate is None or payload.timeout is None:
                raise HTTPException(status_code=400,
                                    detail="UART порт, скорость, таймаут нужны для отправки данных по UART")
            print(
                f"Отправка данных по UART по порту {payload.uartPort} со скоростью {payload.baudRate} и таймаутом {payload.timeout}. Данные: {payload.data}")

        case _:
            raise HTTPException(status_code=400, detail="Неверный метод")

    return {"status": "success", "method": payload.method, "data": payload.data}
