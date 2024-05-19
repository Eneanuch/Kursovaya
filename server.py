import os
from fastapi import FastAPI
from starlette.responses import FileResponse, JSONResponse

app = FastAPI()
root = os.path.dirname(os.path.abspath(__file__))


# run with uvicorn server:app --host 0.0.0.0 --port 80


@app.get('/')
async def results():
    return FileResponse('index.html')


@app.get('/get_results')
async def get_results():
    data = {
        'humidity': '45%',
        'temperature': '22°C',
        'amperage': '3.5A',
        'battery': '75%'
    }
    return JSONResponse(data)
