from fastapi import FastAPI
from datetime import datetime
from typing import List
import schema
import asyncio
import socket
import json
import pickle


signals = []

f = open('../config.json')
data = json.load(f)
data = data
host = '0.0.0.0'
port = 8002
print(data)
for i in data:
    if i["component"] == 'manipulator':
        host = i["host"]
        port = i["port"]


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, 8002))

async def decision_make(signals: List[schema.SensorSignal]) -> schema.ControllerRequest:
    sum_payloads = sum(signal.payload for signal in signals)
    if sum_payloads % 2:
        return schema.ControllerRequest(datetime=datetime.now(), status=schema.Status.UP)
    else:
        return schema.ControllerRequest(datetime=datetime.now(), status=schema.Status.DOWN)


app = FastAPI()


async def send_to_manipulator():
    global signals
    while True:
        await asyncio.sleep(5)
        result = await decision_make(signals)
        result_b = pickle.dumps(result.json())
        s.send(result_b)
        signals = []


@app.post("/sensor")
async def receive_signals(signal: schema.SensorSignal):
    signals.append(signal)
    return signal

@app.on_event("startup")
async def send_data():
    asyncio.create_task(send_to_manipulator())
