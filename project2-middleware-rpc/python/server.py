from flask import Flask
from flask_jsonrpc import JSONRPC

ht = {}

app = Flask(__name__)
jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)

@jsonrpc.method('App.index')
def index() -> str:
    return 'Welcome to Flask JSON-RPC'

@jsonrpc.method('put()')
def put(key: str, value: int) -> None:
    ht[key] = value

@jsonrpc.method('get()')
def put(key: str) -> int:
    return ht[key]

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)



""""
curl -i -X POST \
       -H "Content-Type: application/json; indent=4" \
       -d '{
        "jsonrpc": "2.0",
        "method": "put()",
        "params": { "key": "athus", "value": 3 },
        "id": "1"
    }' http://localhost:5000/api


curl -i -X POST \
       -H "Content-Type: application/json; indent=4" \
       -d '{
        "jsonrpc": "2.0",
        "method": "get()",
        "params": { "key": "athus" },
        "id": "1"
    }' http://localhost:5000/api

"""