#!/usr/bin/env python3

import requests
# from PIL import Image
# from io import BytesIO


payload = {'key1': 'value1', 'key2': 'value2'}
r = requests.post("https://httpbin.org/post", data=payload)
print(r.text)
