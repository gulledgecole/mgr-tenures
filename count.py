import praw
import pandas as pd
import os
from time import sleep

reddit_client = os.environ.get("reddit_client")
reddit_app_pass = os.environ.get("reddit_app_pass")
reddit_user_pass = os.environ.get("reddit_user_pass")
reddit_user = os.environ.get("reddit_user")
# Initialize Reddit instance
reddit = praw.Reddit(
    client_id=reddit_client,
    client_secret=reddit_app_pass,
    username=reddit_user,
    user_agent="mgr-tenures",
)

# Subreddit to scrape
subreddit = reddit.subreddit("ArsenalFC")

post_count = 0
for submission in subreddit.submission():
    post_count += 1

print(f'Total number of posts: {post_count}')