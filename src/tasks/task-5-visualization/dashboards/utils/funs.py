

import pandas as pd
import streamlit as st
from utils.emojis import EmojiCloud
import plotly.express as px


FILES_PATH = "src/data/task-5-visualization"
FONTS_PATH = "src/tasks/task-5-visualization/dashboards/utils/fonts"


def clean_emojis(emoji):
    emoji = emoji.replace("[", "")
    emoji = emoji.replace("]", "")
    emoji = emoji.replace("'", "")
    emoji = emoji.strip()
    return emoji


@st.cache(persist=True)
def load_data(lang, start_date, end_date):
    data = pd.read_csv(f"{FILES_PATH}//Corrected_final_all_with_sentiment.csv")
    data['preprocessed_created_at'] = pd.to_datetime(
        data['preprocessed_created_at'])
    data['Month'] = data.preprocessed_created_at.dt.month.astype(
        str)  # +'_'+ data.preprocessed_created_at.dt.month_name()
    data['Weeknum'] = data.preprocessed_created_at.apply(
        lambda d: (d.day-1) // 7 + 1)
    data['MonthWeek_merged'] = data['Month'] + ' ' + data.Weeknum.astype(str)
    data = data[data["twitter_lang"] == lang]
    data = data[(data["preprocessed_created_at"] >= start_date)
                & (data["preprocessed_created_at"] <= end_date)]
    sentiments = {
        1: "POS",
        0: "NEG",
    }
    data["favorite_count"] = data["favorite_count"].astype(int)
    data["full_text_sentiment"] = data["sentiment_score"].map(sentiments)
    return data


@st.cache(persist=True)
def get_hashtag_counts(data):
    ans = {}
    for _, row in data.iterrows():
        if not pd.isna(row["hashtags"]):
            for hashtag in row["hashtags"].split(" , "):
                ans[hashtag] = ans.get(hashtag.strip(), 0) + 1
    ans = {k: v for k, v in sorted(
        ans.items(), key=lambda item: item[1], reverse=True)}
    return ans


@st.cache(persist=True, suppress_st_warning=True, allow_output_mutation=True)
def get_emojicloud():
    return EmojiCloud(font_path=f"{FONTS_PATH}/TwitterColorEmoji-SVGinOT.ttf")


@st.cache(allow_output_mutation=True)
def get_emojis(data):
    ans = []
    for i in data.emoji_list:
        if i != "['']":
            ans.append(clean_emojis(i))
    return ans

def get_map(tweets):
    locations = pd.read_csv(f"{FILES_PATH}/cleaned_colombian_locations.csv", index_col=[0])
    data = pd.merge(locations, tweets, left_on="User", right_on="user_name")
    #Determine how many times the city is repeated
    df = pd.DataFrame(data.city.value_counts())
    df.reset_index(inplace= True)
    #This is a dataset with the number of city occurences
    df = df.rename(columns={ 'index': 'city' ,'city': 'quantity'})
    #Merge the 2 DF
    data= df.merge(data, how='inner', on='city', validate= '1:m')
    #Calcute the % of ocurrences of each city
    data['Tweets_%'] = round(data['quantity']/len(data['city'])*100, 2)
    #COnvert city's names to Uppercase
    data['city'] = data['city'].str.upper()
    #Map
    px.set_mapbox_access_token("pk.eyJ1IjoiYW5hbGlhMjAyMCIsImEiOiJja3VnbXdpdmcyNWZmMm9uenpsMHVqazM0In0.Q5WfRGaOgxlgJ59yDJiqWw")# Create an account in Map Box, this website allows us to plot better map, We can identify small places not only big cities.
    #Plot the map with plotly library
    fig = px.scatter_mapbox(data, lat="latitude", lon="longitude", color="Tweets_%",hover_name="city", size="Tweets_%",color_continuous_scale=px.colors.sequential.Viridis, zoom=5, height=800, center={"lat":4.5709, "lon":-74.2973})
    fig.update_layout(
        title="Colombia Strike 2021: Tweets",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="Green"
        )
    )
    return fig

def get_all_text(data): 
    ans = ""
    for word_list in data["preprocessed_data_without_hashtags"]:
        word_list = eval(word_list)
        ans+=" ".join(word_list) + " "
    return ans 

def get_sentiment_count(data, hashtag):
    counts = {}
    for _, row in data.iterrows():
        if not pd.isna(row["hashtags"]) and hashtag in row["hashtags"]:
            sentiment = row["full_text_sentiment"]
            counts[sentiment] = counts.get(sentiment, 0) + 1
    ans = pd.DataFrame(data={"Sentiment":counts.keys(), "Frequency": counts.values()})
    return ans
    