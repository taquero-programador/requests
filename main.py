#!/usr/bin/env python3

import requests
import json
# from PIL import Image
# from io import BytesIO


url = 'https://api.github.com/users/taquero-programador'
r = requests.get(url)
print(r.text)
