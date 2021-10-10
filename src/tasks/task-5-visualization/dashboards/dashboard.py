
import os
import datetime
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud
from utils.funs import (load_data, get_hashtag_counts,
                        get_emojicloud, get_emojis, get_map, get_all_text, get_sentiment_count)

CURRENT_PATH = os.path.dirname(__file__)
FILES_PATH = "src/data/task-5-visualization"

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

event_df = pd.read_csv(f'{FILES_PATH}/event_df.csv')
high_event_df = pd.read_csv(f'{FILES_PATH}/high_event_df.csv')
topic_data = pd.read_csv(f"{FILES_PATH}//Corrected_Final_All_sentiment_topics.csv")
topics = pd.read_csv(f"{FILES_PATH}//topic_df.csv", index_col="Topic Number")

st.header("Important dates")

choice = st.selectbox('Select your preference: ', ['Time Range', 'Singular Date'])

if choice == 'Singular Date':
    date = datetime.datetime.strptime('2021-04-28', '%Y-%m-%d')
    start_date = st.date_input('Input start date: ', date, min_value=datetime.date(2021,3,22) , max_value=datetime.date(2021,9,4))
    event = event_df.loc[event_df['Date'] == start_date.strftime('%Y-%m-%d'), 'Event']

    st.markdown(f"""<h4 style='color:#f0f0f0'> Notable event(s) of the day: {start_date.strftime("%Y-%m-%d")}</h4>""", True)
    st.write(' ')

    range_1 = {'start' : datetime.datetime(2021, 4, 28, 0, 0), 'end' : datetime.datetime(2021, 5, 6, 0, 0)}
    range_2 = {'start' : datetime.datetime(2021, 5, 9, 0, 0), 'end' : datetime.datetime(2021, 5, 29, 0, 0)}
    range_3 = {'start' : datetime.datetime(2021, 6, 1, 0, 0), 'end' : datetime.datetime(2021, 6, 11, 0, 0)}
    range_4 = {'start' : datetime.datetime(2021, 6, 8, 0, 0), 'end' : datetime.datetime(2021, 6, 10, 0, 0)}

    str_start_date = start_date.strftime('%Y-%m-%d')
    
    st.markdown('<h5>Event Summary</h5>', True)
    if (str_start_date in pd.date_range(**range_1)):
        high_event = high_event_df.loc[high_event_df['Date'] == str(tuple(range_1.values())), 'Event']

    elif (str_start_date in pd.date_range(**range_2)):
        high_event = high_event_df.loc[high_event_df['Date'] == str(tuple(range_2.values())), 'Event']

    elif (str_start_date in pd.date_range(**range_3)):
        high_event = high_event_df.loc[high_event_df['Date'] == str(tuple(range_3.values())), 'Event']

    elif (str_start_date in pd.date_range(**range_4)):
        high_event = high_event_df.loc[high_event_df['Date'] == str(tuple(range_4.values())), 'Event']

    else:
        high_event = pd.Series()
        pass

    if high_event.empty:
        st.write('None \n ')
    else:
        if len(high_event) != 1:
            high_event = high_event.to_numpy().tolist()
            for e in high_event:
                st.write(f'{high_event.index(e) + 1}. {e}')
        else:
            st.write(f'1. {high_event.values.item()}')

    st.markdown('<h5>Occurent Events</h5>', True)
    if len(event) == 0:
        st.write('None \n ')
    elif len(event) > 1:
        events = event.to_numpy().tolist()
        for e in events:
            st.write(f'{events.index(e) + 1}. {e}')
    else:
        st.write(f'1. {event.values.item()}')
        pass

else:
    dates = ['2021-02-01', '2021-03-01']
    dates = tuple([datetime.datetime.strptime(d, "%Y-%m-%d") for d in dates])

    assert len(dates) == 2 and dates[1] > dates[0]

    start_date = st.date_input('Input start date: ', dates, min_value=datetime.date(2021,3,22) , max_value=datetime.date(2021,9,4))
    event = event_df.loc[event_df['Date'] == dates, 'Event']

    st.markdown(f"""<h4 style='color:#f0f0f0'> Notable event(s) of the day: {start_date[0].strftime("%Y-%m-%d")} to {start_date[1].strftime("%Y-%m-%d")}</h4>""", True)
    st.write(' ')
    
    kwargs = {'start' : start_date[0], 'end' : start_date[1]}
    
    event_dict = {}
    for date in pd.date_range(**kwargs):
        events = event_df.loc[event_df['Date'] == date.strftime('%Y-%m-%d'), 'Event'].to_numpy().tolist()
        event_dict.update({date.strftime('%Y-%m-%d') : events})
    
    if not bool(list(event_dict.values())):
        st.write('No major event for this time frame.')
    else:
        for key in event_dict.keys():
            if not bool(event_dict[key]):
                pass
            else:
                st.markdown(f"""<h5>Day: {key}</h5>""", True)
                for e in event_dict[key]:
                    st.write(f'\t{event_dict[key].index(e) + 1}. ', e)


st.header("Tweets")
# Random tweet by sentiment
st.subheader("Display random tweet")
random_tweet = st.radio('Sentiment', ('POS', 'NEG'))
st.markdown(data.query(
    "full_text_sentiment == @random_tweet")[["full_text"]].sample(n=1).iat[0, 0])


st.subheader("Top 5 most liked tweets")
top_5 = data.sort_values(by="favorite_count", ascending=False)[["preprocessed_created_at","full_text","favorite_count","full_text_sentiment"]].head()
fig = go.Figure(data=[go.Table(
        header=dict(values=list(top_5.columns),
                    align='left'),
        cells=dict(values=[top_5.preprocessed_created_at, top_5.full_text, top_5.favorite_count, top_5.full_text_sentiment],
                   align='left'))
    ])
st.plotly_chart(fig)

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

st.subheader("Sentiments by hashtag")
hashtag = st.selectbox('Select the hashtag: ', list(hashtag_counts.keys())[:50])
sentiment_count_hashtag = get_sentiment_count(data, hashtag)
fig = px.bar(sentiment_count_hashtag, x='Sentiment',
                    y='Frequency', color='Frequency', height=500, color_continuous_scale=px.colors.sequential.Viridis)
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




####Topic Modelling Style Chart

st.header("Topics")

st.table(topics)
topic_dim = go.parcats.Dimension(values=topic_data.Dominant_Topic, label="Topic")

sentiment_dim = go.parcats.Dimension(
    values=topic_data.sentiment_score, label="Sentiment", categoryarray=[0,1],
    ticktext=['Negative', 'Positive']
)

# Create parcats trace
color = topic_data.sentiment_score
colorscale = [[0, 'firebrick'], [1, 'mediumseagreen']];

fig = go.Figure(data = [go.Parcats(dimensions=[ topic_dim, sentiment_dim],
        line={'color': color, 'colorscale': colorscale},
        hoveron='color', hoverinfo='count+probability',
        labelfont={'size': 18, 'family': 'Times'},
        tickfont={'size': 16, 'family': 'Times'},
        arrangement='freeform')])

st.plotly_chart(fig)

st.subheader("Words by topic")
image = Image.open(f"{CURRENT_PATH}/media/topics.png")
st.image(image)
