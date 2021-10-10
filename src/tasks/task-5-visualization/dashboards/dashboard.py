
import os
import datetime
import pandas as pd
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from utils.funs import (load_data, get_hashtag_counts,
                        get_emojicloud, get_emojis, get_map, get_all_text)

CURRENT_PATH = os.path.dirname(__file__)

LANGUAGES = {
    "Spanish": "es",
    "English": "en"
}

st.title("Colombia social network analysis during strike")
st.markdown("-by Omdena")
st.sidebar.title("Sentiment Analysis of Tweets/Reddit messages")
st.markdown("Streamlit based interactive dashboard used ")
st.sidebar.markdown("Streamlit based interactive dashboard used "
                    "to analyze sentiments of tweets 🐦 and Reddit threads")

language = st.sidebar.selectbox(
'Language',
('Spanish', 'English'))

start_date = st.sidebar.date_input( "Start date", value = datetime.date(2021,3,22), min_value=datetime.date(2021,3,22) , max_value=datetime.date(2021,9,4)).isoformat()
end_date =  st.sidebar.date_input( "End date", value = datetime.date(2021,9,4), min_value=datetime.date(2021,3,22) , max_value=datetime.date(2021,9,4)).isoformat()

data = load_data(LANGUAGES[language], start_date, end_date)
hashtag_counts = get_hashtag_counts(data)
emoji_cloud = get_emojicloud()

st.header("Tweets")

# Random tweet by sentiment
st.subheader("Display random tweet")
random_tweet = st.radio('Sentiment', ('POS', 'NEG'))
st.markdown(data.query(
    "full_text_sentiment == @random_tweet")[["full_text"]].sample(n=1).iat[0, 0])


###monthly stuff 
grouped_data = data.groupby(['MonthWeek_merged']).aggregate({
                                    'favorite_count':'sum','sentiment_score':'mean','full_text':'nunique'}).reset_index()

grouped_data.sentiment_score = grouped_data.sentiment_score.apply(lambda x: x*100)
new = grouped_data["MonthWeek_merged"].str.split(" ", n = 1, expand = True)
grouped_data["Month_Num"]= new[0]
grouped_data["MW"]= new[1]


# fig = go.Figure()
fig = px.line(grouped_data, x='MonthWeek_merged', y=['favorite_count','full_text']
             )
# fig.add_trace(go.Scatter(
#                         #x = cust["Original x-axis"], 
#                         x = [grouped_data["Month_Num"],grouped_data["MW"]],
#                       y = grouped_data['favorite_count'], mode = "lines"))
# # ,grouped_data['full_text']
# fig.add_trace(go.Scatter(
#                         #x = cust["Original x-axis"], 
#                         x = [grouped_data["Month_Num"],grouped_data["MW"]],
#                       y = grouped_data['full_text'], mode = "lines"))   
fig.update_layout(barmode = 'stack', xaxis={'categoryorder':'category ascending'},xaxis_tickangle=-45)  
st.plotly_chart(fig)


fig = px.bar(grouped_data, x="MonthWeek_merged", y=['full_text']
             , color='sentiment_score', color_continuous_scale=px.colors.sequential.Viridis)

fig.update_layout(barmode = 'stack', xaxis={'categoryorder':'category ascending'},xaxis_tickangle=-45)  
st.plotly_chart(fig)

col1, col2 = st.columns(2)
# Emojis wordcloud
col1.subheader("Emoji cloud")
emojis = get_emojis(data)
fig, ax = plt.subplots()
wc = emoji_cloud.generate(emojis)
im = ax.imshow(wc,interpolation="bilinear")
ax.axis("off")
col1.pyplot(fig)

col2.subheader("Word cloud")
tweets_text = get_all_text(data)
fig = plt.figure(figsize = (20, 10))
img = WordCloud(max_font_size = 100).generate(tweets_text)
plt.imshow(img, interpolation = 'bilinear')
plt.xticks([]); plt.yticks([])
col2.pyplot(fig)

st.subheader("Tweets map")
map_fig = get_map(data)
st.plotly_chart(map_fig)

st.header("Sentiment")
# Tweets by sentiment
st.markdown("### Total Number of tweets by sentiment")
select = st.selectbox('Type of visualization', [
    'Bar plot', 'Pie chart'], key='1')
sentiment_count = data['full_text_sentiment'].value_counts()
sentiment_count = pd.DataFrame(
    {'Sentiment': sentiment_count.index, 'Tweets': sentiment_count.values})
# move to plotting
st.markdown("### Number of tweets by sentiment")
if select == 'Bar plot':
    fig = px.bar(sentiment_count, x='Sentiment',
                    y='Tweets', color='Tweets', height=500, color_continuous_scale=px.colors.sequential.Viridis)
    st.plotly_chart(fig)
else:
    fig = px.pie(sentiment_count, values='Tweets', names='Sentiment')
    st.plotly_chart(fig)

st.subheader("Sentiment bar chart race")
st.video(f"{CURRENT_PATH}/media/sentiment_bcr_{LANGUAGES[language]}.mp4")

st.header("Hashtags")
st.subheader("Hashtags bar chart race")
st.video(f"{CURRENT_PATH}/media/hashtag_bcr_{LANGUAGES[language]}.mp4")

hashtags_to_consider = st.slider(
    "Hashtags to look at", 5, min(50, len(hashtag_counts)))
hashtags = [hashtag for hashtag in hashtag_counts.keys()]
tweets = [hashtag for hashtag in hashtag_counts.values()]
hashtag_sentiment_count = pd.DataFrame(
    {'Hashtag': hashtags[:hashtags_to_consider], 'Tweets': tweets[:hashtags_to_consider]})
st.subheader("Total number of tweets for each hashtag")
fig_1 = px.bar(hashtag_sentiment_count, x='Hashtag',
                y='Tweets', color='Tweets', height=500, color_continuous_scale=px.colors.sequential.Viridis)
st.plotly_chart(fig_1)


