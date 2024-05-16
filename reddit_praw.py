import praw
import pandas as pd
import os 
from time import sleep 

reddit_client = os.environ.get("reddit_client")
reddit_app_pass = os.environ.get("reddit_app_pass")
reddit_user_pass = os.environ.get("reddit_user_pass")
reddit_user = os.environ.get("reddit_user")
# Initialize Reddit instance
reddit = praw.Reddit(client_id=reddit_client,
                     client_secret=reddit_app_pass,
                     username = reddit_user,
                     user_agent="mgr-tenures")

# Subreddit to scrape
subreddit = reddit.subreddit('ArsenalFC')


# Define lists to store data
data = []

# Scraping posts & Comments
for post in subreddit.new(limit= 1000): 
    data.append({
        'Type': 'Post',
        'Post_id': post.id,
        'Title': post.title,
        'Author': post.author.name if post.author else 'Unknown',
        'Timestamp': post.created_utc,
        'Text': post.selftext,
        'Score': post.score,
        'Total_comments': post.num_comments,
        'Post_URL': post.url
    })

# Check if the post has comments
    if post.num_comments > 0:
        # Scraping comments for each post
        post.comments.replace_more(limit= None)
        sleep(2)
        for comment in post.comments.list():
            data.append({
                'Type': 'Comment',
                'Post_id': post.id,
                'Title': post.title,
                'Author': comment.author.name if comment.author else 'Unknown',
                'Timestamp': pd.to_datetime(comment.created_utc, unit='s'),
                'Text': comment.body,
                'Score': comment.score,
                'Total_comments': 0, #Comments don't have this attribute
                'Post_URL': None  #Comments don't have this attribute
            })

# Create pandas DataFrame for posts and comments
data = pd.DataFrame(data)
data.to_csv("arsenalFC.csv")