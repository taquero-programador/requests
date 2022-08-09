#!/usr/bin/env python3

import requests
import json
# from PIL import Image
# from io import BytesIO


url = 'https://httpbin.org/cookies'
cookies = dict(cookies_are='working')
r = requests.get(url, cookies=cookies)
print(r.text)
