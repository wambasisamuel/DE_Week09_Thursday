import praw
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from credentials import CLIENT_ID, CLIENT_SECRET, USER_AGENT


def stream_data(subred):
    search_terms = ["telecom scam","phone fraud","billing fraud","identity theft","sim swap"]
    stream = subred.stream.comments(skip_existing=True)
    df = pd.DataFrame(columns=['author', 'subreddit', 'time', 'comment'])

    for comment in stream:
        try:
            post = comment.submission.selftext
            comment_body = comment.body
            if any(term in comment_body.lower() for term in search_terms):
                data = {
                        "author": str(comment.author),
                        "subreddit": comment.subreddit,
                        "time": datetime.utcfromtimestamp(int(comment.created_utc)).strftime('%Y-%m-%d %H:%M:%S'),
                        "comment": comment_body
                    }
                df = df.append(data, ignore_index=True)

        except praw.exceptions.PRAWException as e:
            pass

    return df


reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT
        )

subreddit = reddit.subreddit('all')

df_stream = stream_data(subreddit)


# Count comments by subreddit
subreddit_counts = df_stream.groupby('subreddit')['subreddit'].count()

# Bar chart for the number of comments per subreddit
plt.figure(figsize=(10, 6))
plt.bar(subreddit_counts.index, subreddit_counts.values)
plt.title('Number of Comments per Subreddit')
plt.xlabel('Subreddit')
plt.ylabel('Number of comments')
plt.show()
