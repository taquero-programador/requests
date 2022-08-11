#!/usr/bin/env python3

import requests

payload = {'username': 'corey', 'password': 'testing'}
url = 'https://httpbin.org/post'
r = requests.post(url, data=payload)

r_dict = r.json()
print(r_dict['form'])
