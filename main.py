#!/usr/bin/env python3

import requests
from requests.auth import HTTPBasicAuth
import csv
import praw
import time

inicio = time.time()

CLIENT_ID = 'id'
SECRET_KEY = 'key'
headers = {'User-Agent': 'teddi/0.0.1'}
reddit = praw.Reddit(
    client_id = CLIENT_ID,
    client_secret = SECRET_KEY,
    password = 'pass',
    user_agent = headers,
    username = 'fake_user',
)
# con la configuración anterior se obtiene accedo como usario, para esto ademas del client_id y secret se requiere user y pass

sub = reddit.subreddit('python') # obtiene el sub
# print(sub.display_name) # obtiene el nomre del sub
# print(sub.title)

# iterar sobre el sub. controversial, gilded, hot, new, rising, top
# acceder a los 10 primeros usando limit
comms = reddit.submission("id_post")
comms.comments_sort = "new"
top = list(comms.comments)

with open('reddit.csv', 'w', newline='') as f:
    esc = csv.writer(f)
    esc.writerow(['RSUB', 'USERNAME', 'COMMENTS', 'UPS', 'TITLE_POST'])
    for subs in sub.hot():
        print("################")
        print(subs.title)
        print(subs.url)
        # print(vars(subs))
        for i in subs.comments:
            data = subs.subreddit, i.author, i.body, i.ups, subs.title
            esc.writerow(data)

fin = time.time() - inicio
ok_time = fin/60
print(f"Done! - Tiempo: {ok_time:.2f}")
