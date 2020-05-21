#!/usr/bin/python3
import flask
import json
import time
from functools import wraps
from flask import request, jsonify, abort


app = flask.Flask(__name__)
HOST = '0.0.0.0'
PORT = 5000


# sample api keys
# change with authentication function
API_KEYS = [
    '5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9',
    '6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b',
    'd4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35',
    '4e07408562bedb8b60ce05c1decfe3ad16b72230967de01f640b7e4729b49fce',
    '4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a',
    'ef2d127de37b942baad06145e54b0c619a1f22327b2ebbcfbec78f5564afe39d',
    'e7f6c011776e8db7cd330b54174fd76f7d0216b612387a5ffcfb81e6f0919683',
    '7902699be42c8a8e46fbbb4501726517e86b22c56a189f7625a6da49081b2451',
    '2c624232cdd221771294dfbb310aca000a0df6ac8b66b696d90ef06fdefb64a3',
    '19581e27de7ced00ff1ce50b2047e7a567c76b1cbaebabe5ef03f7c3017bb5b7',
]

# api authentication decorator
def require_api_key(func):
    @wraps(func) 
    def inner_function(*args, **kwargs):
        if 'api-key' in request.headers and (request.headers['api-key'] in API_KEYS):
            return func(*args, **kwargs)
        else:
            abort(401)
    return inner_function


@app.route('/', methods=['GET'])
def home():
    return "<h1>Sensor Data Archive</h1><p>This site is a demo API for distant reading of sensor data with HTTP header authentication.</p>"


# A route to return all of the available entries in our catalog.
@app.route('/api/v1/resources/sensors/all', methods=['GET'])
@require_api_key
def api_all():
    with open('data.json') as file:
        data = json.load(file)
    data['status_code'] = 0
    data['timestamp'] = time.time()
    return jsonify(data)


@app.route('/api/v1/resources/sensors', methods=['GET'])
@require_api_key
def api_id():
    # example usage to get data of sensor id 1
    # /api/v1/resources/sensors?id=1

    with open('data.json') as file:
        data = json.load(file)

    if 'id' in request.args:
        _id = int(request.args['id'])
    else:
        abort(404)

    response = dict()
    response['results'] = []

    for sensor in data['sensors']:
        if sensor['id'] == _id:
             response['results'].append(sensor)

    response['status_code'] = 0
    response['timestamp'] = time.time()
    return jsonify(response)


def main():
    app.config["DEBUG"] = True
    app.run(HOST, PORT)


if __name__ == '__main__':
    main()