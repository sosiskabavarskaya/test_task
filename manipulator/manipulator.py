import socket
import json
import logging
import pickle
from datetime import datetime

logging.basicConfig(filename='logs/logs.log', encoding='utf-8', level=logging.DEBUG)
f = open('../config.json')
data = json.load(f)
data = data
host = ''
port = 0
for i in data:
    if i["component"] == 'manipulator':
        host = i["host"]
        port = i["port"]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", port))
s.listen()

while True:
    client_s, address = s.accept()
    print(f"incomming data from {address}")
    while True:
        data = client_s.recv(2048)
        if not data:
            continue
        res = pickle.loads(data)
        print("Received row: " + res)
        logging.info(f'{datetime.now()} - Received row: {res}')
