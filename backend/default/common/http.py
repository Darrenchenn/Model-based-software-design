import json

import requests


def request(url, method, payload):
    payload = json.dumps(payload)
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request(method, url, headers=headers, data=payload)
    return response.json()
