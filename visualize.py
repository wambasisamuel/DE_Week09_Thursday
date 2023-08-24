import praw
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
from datetime import datetime
from credentials import CLIENT_ID, CLIENT_SECRET, USER_AGENT


def stream_comments(subred):
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


# Define function to visualize data in a meaningful way
def visualize(df):
    st.write("Number of fraud mentions by location")
    subreddit_counts = df['subreddit'].value_counts()
    fig, ax = plt.subplots()
    sns.barplot(x=subreddit_counts.values, y=subreddit_counts.index, ax=ax)
    ax.set_xlabel('Number of comments')
    ax.set_ylabel('Subreddit')
    st.pyplot(fig)

# Set up Streamlit app
st.title("Reddit Fraud Comments Dashboard")


reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT
        )

subreddit = reddit.subreddit('all')

# Stream comments
df_stream = stream_comments(subreddit)

# Visualize in Streamlit
visualize(df_stream)
