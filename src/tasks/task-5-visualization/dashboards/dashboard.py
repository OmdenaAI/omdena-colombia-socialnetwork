
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import matplotlib.pyplot as plt
from utils.funs import (load_data, get_hashtag_counts,
                        get_emojicloud, get_emojis_by_week)

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

data = load_data(LANGUAGES[language])
hashtag_counts = get_hashtag_counts(data)
emoji_cloud = get_emojicloud()



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
             , color='sentiment_score')

fig.update_layout(barmode = 'stack', xaxis={'categoryorder':'category ascending'},xaxis_tickangle=-45)  
st.plotly_chart(fig)





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
                    y='Tweets', color='Tweets', height=500)
    st.plotly_chart(fig)
else:
    fig = px.pie(sentiment_count, values='Tweets', names='Sentiment')
    st.plotly_chart(fig)

st.header("Hashtags")
st.subheader("Hashtags bar race")
st.video(f"{CURRENT_PATH}/media/both_languages.mp4")

hashtags_to_consider = st.slider(
    "Hashtags to look at", 1, min(50, len(hashtag_counts)))
hashtags = [hashtag for hashtag in hashtag_counts.keys()]
tweets = [hashtag for hashtag in hashtag_counts.values()]
hashtag_sentiment_count = pd.DataFrame(
    {'Hashtag': hashtags[:hashtags_to_consider], 'Tweets': tweets[:hashtags_to_consider]})
st.subheader("Total number of tweets for each hashtag")
fig_1 = px.bar(hashtag_sentiment_count, x='Hashtag',
                y='Tweets', color='Tweets', height=500)
st.plotly_chart(fig_1)


# Emojis wordcloud
st.subheader("Emojis by week")
weeks_to_consider = st.slider(
    "Weeks to look at", 1, int(data["preprocessed_created_at"].dt.week.max()))
emojis = get_emojis_by_week(data, weeks_to_consider)
st.subheader("Emoji cloud for each week")
fig, ax = plt.subplots()
wc = emoji_cloud.generate(emojis)
im = ax.imshow(wc,interpolation="bilinear")
ax.axis("off")
st.pyplot(fig)

