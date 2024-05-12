
import os
import requests
import pandas as pd

# note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
reddit_client = os.environ.get("reddit_client")
reddit_app_pass = os.environ.get("reddit_app_pass")
reddit_user_pass = os.environ.get("reddit_user_pass")
reddit_user = os.environ.get("reddit_user")
auth = requests.auth.HTTPBasicAuth(reddit_client, reddit_app_pass)
print(auth)
# here we pass our login method (password), username, and password
data = {'grant_type': 'password',
        'username':reddit_user,
        'password': reddit_user_pass}
# setup our header info, which gives reddit a brief description of our app
headers = {'User-Agent': 'MyBot/0.0.1'}

# send our request for an OAuth token
res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)

# convert response to JSON and pull access_token value
TOKEN = res.json()['access_token']

# add authorization to our headers dictionary
headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

# # while the token is valid (~2 hours) we just add headers=headers to our requests

res = requests.get("https://oauth.reddit.com/r/ArsenalFC/new",
                   headers=headers)
for post in res.json()['data']['children']:
    print(post)