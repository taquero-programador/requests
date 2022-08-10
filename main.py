#!/usr/bin/env python3


import requests
import json
from requests.auth import HTTPBasicAuth

auth = HTTPBasicAuth('taquero-programador', 'no_pass')
body = ({u"body": u"Sounds great! I'll get right on it!"})
url = u"https://api.github.com/repos/psf/requests/issues/482/comments"
r = requests.post(url, data=body, auth=auth)
print(r.status_code)
