#!/usr/bin/python3
import requests
import random
from hashlib import sha256


def main():
    # test get all sensor data
    key = sha256(bytes(f'{random.randint(0, 9)}', 'utf-8')).hexdigest()
    url = 'http://127.0.0.1:5000/api/v1/resources/sensors/all'
    reply = requests.get(url, headers={'api-key': key})
    assert reply.status_code == 200
    print(reply.text)

    # test get data of sensor id 1
    url = 'http://127.0.0.1:5000/api/v1/resources/sensors?id=1'
    reply = requests.get(url, headers={'api-key': key})
    assert reply.status_code == 200
    print(reply.text)

    # test open api
    url = 'http://127.0.0.1:5000/'
    reply = requests.get(url)
    assert reply.status_code == 200

    # test get data w/o api-key in headers
    url = 'http://127.0.0.1:5000/api/v1/resources/sensors?id=1'
    reply = requests.get(url)
    assert reply.status_code == 401

    # test unknown url
    url = 'http://127.0.0.1:5000/foo-bar'
    reply = requests.get(url)
    assert reply.status_code == 404


if __name__ == '__main__':
    main()