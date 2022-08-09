#!/usr/bin/env python3

import requests
import json


url = "https://jsonplaceholder.typicode.com/todos"
todo = {
    'userId': 1,
    'title': 'Buy milk',
    'completed': False
}
r = requests.post(url, data=json.dumps(todo), headers={'Content-Type': 'application/json'})
print(r.text, r.status_code)
