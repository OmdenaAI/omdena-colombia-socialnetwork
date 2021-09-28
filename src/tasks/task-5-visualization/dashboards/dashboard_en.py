
import pandas as pd
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt
from utils.funs import (load_data, get_hashtag_counts,
                        get_emojicloud, get_emojis_by_week)

st.title("Colombia social network analysis during strike")
st.markdown("-by Omdena")
st.sidebar.title("Sentiment Analysis of Tweets/Reddit messages")
st.markdown("Streamlit based interactive dashboard used ")
st.sidebar.markdown("Streamlit based interactive dashboard used "
                    "to analyze sentiments of tweets 🐦 and Reddit")

data = load_data("en")
hashtag_counts = get_hashtag_counts(data)
emoji_cloud = get_emojicloud()

# Random tweet by sentiment
st.sidebar.subheader("Display random tweet")
random_tweet = st.sidebar.radio('Sentiment', ('POS', 'NEU', 'NEG'))
st.sidebar.markdown(data.query(
    "full_text_sentiment == @random_tweet")[["full_text"]].sample(n=1).iat[0, 0])

# Tweets by sentiment
st.sidebar.markdown("### Total Number of tweets by sentiment")
select = st.sidebar.selectbox('Type of visualization', [
    'Bar plot', 'Pie chart'], key='1')
sentiment_count = data['full_text_sentiment'].value_counts()
sentiment_count = pd.DataFrame(
    {'Sentiment': sentiment_count.index, 'Tweets': sentiment_count.values})

# move to plotting
if not st.sidebar.checkbox("Hide", True):  # by defualt hide the checkbar
    st.markdown("### Number of tweets by sentiment")
    if select == 'Bar plot':
        fig = px.bar(sentiment_count, x='Sentiment',
                     y='Tweets', color='Tweets', height=500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count, values='Tweets', names='Sentiment')
        st.plotly_chart(fig)

# Tweets per hashtag
st.sidebar.subheader("Total number of tweets for each hashtag")
each_hashtag = st.sidebar.selectbox(
    'Type of visualization', ['Bar plot', 'Pie chart'], key='2')
hashtags_to_consider = st.sidebar.slider(
    "Hashtags to look at", 0, len(hashtag_counts))
hashtags = [hashtag for hashtag in hashtag_counts.keys()]
tweets = [hashtag for hashtag in hashtag_counts.values()]
hashtag_sentiment_count = pd.DataFrame(
    {'Hashtag': hashtags[:hashtags_to_consider], 'Tweets': tweets[:hashtags_to_consider]})
if not st.sidebar.checkbox("Close", True, key='21'):
    if each_hashtag == 'Bar plot':
        st.subheader("Total number of tweets for each hashtag")
        fig_1 = px.bar(hashtag_sentiment_count, x='Hashtag',
                       y='Tweets', color='Tweets', height=500)
        st.plotly_chart(fig_1)
    if each_hashtag == 'Pie chart':
        st.subheader("Total number of tweets for each hashtag")
        fig_2 = px.pie(hashtag_sentiment_count,
                       values='Tweets', names='Hashtag')
        st.plotly_chart(fig_2)

# Emojis wordcloud
st.sidebar.subheader("Emojis by week")
weeks_to_consider = st.sidebar.slider(
    "Hashtags to look at", 1, int(data["preprocessed_created_at"].dt.week.max()))
emojis = get_emojis_by_week(data, weeks_to_consider)
if not st.sidebar.checkbox("Close", True, key='31'):
    st.subheader("Emoji cloud for each week")
    fig, ax = plt.subplots()
    wc = emoji_cloud.generate(emojis)
    im = ax.imshow(wc.recolor(color_func=emoji_cloud.color_func, random_state=42),
                   interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)
