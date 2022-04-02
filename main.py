import praw
from difflib import SequenceMatcher
from dotenv import load_dotenv
import os

from medium import *

load_dotenv()
reddit = praw.Reddit(
    client_id=os.getenv('client_id'),
    client_secret=os.getenv('client_secret'),
    password=os.getenv('password'),
    user_agent=os.getenv('user_agent'),
    username=os.getenv('bot_username'),
    )

subreddit = reddit.subreddit("popular")


def main():
    for submission in subreddit.stream.submissions():
        username = submission.author.name
        results = findLink(submission)
        if results != []:
            response = ""
            for result in results:
                medium = Medium(result)
                response = response + (medium.response()) + "\n\n "
                ratio = SequenceMatcher(None, username, medium.author).ratio()
                if ratio > .7:
                    response = response + ("The usernames are pretty similar - {}, {}\n ".format(username,medium.author))
            beenhere = 0
            for comment in submission.comments:
                if comment.author == 'UghMedium':
                    beenhere = 1
            if beenhere == 0:
                submission.reply(body=response)


main()