#!/usr/bin/env python3


import requests
import json

url = 'https://api.github.com/repos/psf/requests/issues/482'
r = requests.get(url)
print(r.status_code)

issue = json.loads(r.text)
print(issue['title'])
print(issue['comments'])
for k,v in issue.items():
    print(v)
