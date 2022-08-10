#!/usr/bin/env python3

import requests

api_url = "https://jsonplaceholder.typicode.com/todos/10"
r = requests.get(api_url)
print(r.json())

todo = {
    'userId': 1,
    'title': 'Wash car',
    'completed': True
}
r = requests.put(api_url, json=todo)
print(r.json())
print(r.status_code)

todo = {'title': 'Mow lawn'}
r = requests.patch(api_url, json=todo)
print(r.json())

r = requests.delete(api_url)
print(r.json())
print(r.status_code)
