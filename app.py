import os
import praw
from time import sleep
import webbrowser
import configparser
import pandas as pd


def setup():
    # if os.path.exists("./scraper.ini"):
    #     print("Found necessary files, starting scraper.")
    #     return
    # else:
    print("Setting up first time configuration...")
    sleep (2)
    webbrowser.open("https://www.reddit.com/prefs/apps")
    config = configparser.ConfigParser()

    config['DEFAULT']['path'] = os.path.join(os.path.abspath,'scraper.py')
    print(f"Creating {config['DEFAULT']['path']}")
    cfg = [
        "bot_name=thematic_scraper",
        "bot_version=2.2.0",
        "bot_author=da_Nif7y",
        "client_id=QSz7vgteaO2JfsiHZNz0ng",
        "client_secret=VIw3QpFtpPpH0xPIetYugfVcPaLeUg",
        "user_agent=%(bot_name)s:v%(bot_version)s (by u/%(bot_author)s)"
    ]

    with open('scraper.ini', 'w') as cf:
        config.write(cf)


def scrape():
    reddit = praw.Reddit(client_id="SHbwgSsuYfVDbEQtWWCxGA", client_secret="dDU3odgce1SLIwKWJV9qd284GcKoog",
                       user_agent="Scuzzydude", timeout = 59)
    comments = 0
    posts = []
    ml_subreddit = reddit.subreddit('australia')
    for post in ml_subreddit.search(query="indigenous voice", sort="top", time_filter="year", limit=10):
        posts.append([post.title, post.score, post.author, post.id, post.num_comments, post.selftext, post.created_utc, post.url])
        
        print(post.selftext, '\n', post.id)
        
        submission = reddit.submission(id=post.id)
        submission.comments.replace_more(limit=None)
        
        for comment in submission.comments.list():
            comments = []
            comments.append([post.title, comment.score, comment.author, comment.id, comment.parent_id, comment.body, comment.created_utc])

        # posts.append(["~~~~~~~", "~~~~~~~", "~~~~~~~", "~~~~~~~", "~~~~~~~","~~~~~~~", "~~~~~~~" ])
    posts = pd.DataFrame(posts, columns=['title_of_parent', 'updoots', 'id', 'author', 'num_comments/parent_comment', 'content', 'date_created', 'url'])

    print(f"posts found: {len(posts)}\ncomments from posts:{comments}")

    # posts.to_csv('australia_top_indigvoi_top102.csv', encoding='utf-8', index=False)

if __name__ == "__main__":
    setup()
    scrape()