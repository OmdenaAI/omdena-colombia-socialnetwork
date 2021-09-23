
import pandas as pd
import plotly.express as px
import streamlit as stml

FILE_PATH = "src/data/task-5-visualization/sentiment_spanish_df.csv"
stml.title("Colombia social network analysis during strike")
stml.markdown("-by Omdena")
stml.sidebar.title("Sentiment Analysis of Tweets/Reddit messages")
stml.markdown("Streamlit based interactive dashboard used ")
stml.sidebar.markdown("Streamlit based interactive dashboard used "
                      "to analyze sentiments of tweets 🐦 and Reddit")


@stml.cache(persist=True)
def load_data():
    data = pd.read_csv(FILE_PATH)
    data['preprocessed_created_at'] = pd.to_datetime(
        data['preprocessed_created_at'])
    return data


@stml.cache(persist=True)
def get_hashtag_counts(data):
    ans = {}
    for _, row in data.iterrows():
        if not pd.isna(row["hashtags"]):
            for hashtag in row["hashtags"].split(" , "):
                ans[hashtag] = ans.get(hashtag.strip(), 0) + 1
    ans = {k: v for k, v in sorted(
        ans.items(), key=lambda item: item[1], reverse=True)}
    return ans


data = load_data()
hashtag_counts = get_hashtag_counts(data)

# Random tweet by sentiment
stml.sidebar.subheader("Display random tweet")
random_tweet = stml.sidebar.radio('Sentiment', ('POS', 'NEU', 'NEG'))
stml.sidebar.markdown(data.query(
    "full_text_sentiment == @random_tweet")[["full_text"]].sample(n=1).iat[0, 0])

# Tweets by sentiment
stml.sidebar.markdown("### Total Number of tweets by sentiment")
select = stml.sidebar.selectbox('Type of visualization', [
                                'Bar plot', 'Pie chart'], key='1')
sentiment_count = data['full_text_sentiment'].value_counts()
sentiment_count = pd.DataFrame(
    {'Sentiment': sentiment_count.index, 'Tweets': sentiment_count.values})

# move to plotting
if not stml.sidebar.checkbox("Hide", True):  # by defualt hide the checkbar
    stml.markdown("### Number of tweets by sentiment")
    if select == 'Bar plot':
        fig = px.bar(sentiment_count, x='Sentiment',
                     y='Tweets', color='Tweets', height=500)
        stml.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count, values='Tweets', names='Sentiment')
        stml.plotly_chart(fig)

# Tweets per hashtag
stml.sidebar.subheader("Total number of tweets for each hashtag")
each_airline = stml.sidebar.selectbox(
    'Type of visualization', ['Bar plot', 'Pie chart'], key='2')
hashtags_to_consider = stml.sidebar.slider(
    "Hashtags to look at", 0, len(hashtag_counts))
hashtags = [hashtag for hashtag in hashtag_counts.keys()]
tweets = [hashtag for hashtag in hashtag_counts.values()]
hashtag_sentiment_count = pd.DataFrame(
    {'Hashtag': hashtags[:hashtags_to_consider], 'Tweets': tweets[:hashtags_to_consider]})
if not stml.sidebar.checkbox("Close", True, key='21'):
    if each_airline == 'Bar plot':
        stml.subheader("Total number of tweets for each hashtag")
        fig_1 = px.bar(hashtag_sentiment_count, x='Hashtag',
                       y='Tweets', color='Tweets', height=500)
        stml.plotly_chart(fig_1)
    if each_airline == 'Pie chart':
        stml.subheader("Total number of tweets for each hashtag")
        fig_2 = px.pie(hashtag_sentiment_count,
                       values='Tweets', names='Hashtag')
        stml.plotly_chart(fig_2)
