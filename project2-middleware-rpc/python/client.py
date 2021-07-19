import requests
import json
from multiprocessing import Pool

url = "http://localhost:5000/api"
headers = { "Content-Type": "application/json" }

def put(key, value):
    payload = { 'jsonrpc': '2.0', 'id': '1',
                'method': 'put()',
                'params': { 'key': key, 'value': value } }
    data = json.dumps(payload)

    response = requests.request("POST", url, data=data, headers=headers)
    return response.json()

def get(key):
    payload = { 'jsonrpc': '2.0', 'id': '1', 
                'method': 'get()',
                'params': { 'key': key } }
    data = json.dumps(payload)

    response = requests.request("POST", url, data=data, headers=headers)
    return response.json()['result'] 



if __name__ == '__main__':
    m = 1000
    processos = 1
    keys = []
    values = []

    # gera os valores
    for i in range(m):
        keys.append(str(i))
        values.append(i)

    # insere os valores
    with Pool(processos) as p:
        p.starmap(put, zip(keys, values))

    # recupera os valores
    with Pool(processos) as p:
        print(p.map(get, keys))