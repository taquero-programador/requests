#!/usr/bin/env python3

import requests
#import json

url = 'https://httpbin.org/post'
fil = {'file': open('foo.png', 'rb'), 'file2': open('bar.png', 'rb')}

r = requests.post(url, files=fil)
print(r.text)
