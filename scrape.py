import praw
import sqlite3
import pandas as pd

from setup import setup


def scrape(ini_data: dict) -> None:
    '''scrapes reddit forums for posts by random ids'''
    reddit = praw.Reddit(client_secret=ini_data['secret'],
                        client_id=ini_data['id'],
                        user_agent=ini_data['user_agent'],
                        timeout=ini_data['timeout'],
                        config_interpolation="basic")
    
    print(f"Reddit connection generated correctly: {reddit.read_only}")

    replies = 0
    posts = []

    ml_subreddit = reddit.subreddit('australia')
    for post in ml_subreddit.search(query="indigenous voice", sort="top", time_filter="year", limit=10):
        posts.append([post.title, post.score, post.author, post.id,
                     post.num_comments, post.selftext, post.created_utc, post.url])

        print(post.selftext, '\n', post.id)

        submission = reddit.submission(id=post.id)
        submission.comments.replace_more(limit=None)

        for comment in submission.comments.list():
            comments = []
            comments.append([comment.id,
                             post.title,
                             comment.score,
                             comment.author,
                             comment.parent_id,
                             comment.body,
                             comment.created_utc])

        # posts.append(["~~~~~~~", "~~~~~~~", "~~~~~~~", "~~~~~~~", "~~~~~~~","~~~~~~~", "~~~~~~~" ])
    posts = pd.DataFrame(posts, columns=['title_of_parent',
                                         'updoots',
                                         'id',
                                         'author',
                                         'num_comments/parent_comment',
                                         'content',
                                         'date_created',
                                         'url'])

    print(f"Posts found: {len(posts)}\nComments from posts:{replies}")

    posts.to_sql('australia_top_indigvoi_top102.csv',
                encoding='utf-8', 
                index=False)


if __name__ == "__main__":
    ini_data = setup()
    scrape(ini_data)
