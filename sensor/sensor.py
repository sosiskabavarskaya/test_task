import random
import requests
import time
import multiprocessing as mp
import datetime
import json

def read_data():

    try:
        f = open("../config.json")
        data = json.load(f)
        for i in data:
            if i["component"] == "controller":
                host = i["host"]
                port = i["port"]
                return host, port
    except IOError:
        print("Can't read configure file")


def make_request(host, port):

    while True:
        url = 'http://' + host + ':' + str(port) + '/sensor'
        obj = {"datetime": datetime.datetime.now().__str__(), 
            "payload": random.choice([0, 1])}
        requests.post(url, json = obj)
        time.sleep(1 / 300)
        

if __name__ == "__main__":
    host, port = read_data()

    print("Started")
    processes = [mp.Process(target=make_request, args=(host, port)) for i in range(8)]

    for process in processes:
        process.start()

    for process in processes:
        process.join()
