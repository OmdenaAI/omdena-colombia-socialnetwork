

import pandas as pd
import streamlit as st
from utils.emojis import EmojiCloud

FILE_PATH = "src/data/task-5-visualization/Corrected_final_all_with_sentiment.csv"
FONTS_PATH = "src/tasks/task-5-visualization/dashboards/utils/fonts"


def clean_emojis(emoji):
    emoji = emoji.replace("[","")
    emoji = emoji.replace("]","")
    emoji = emoji.replace("'","")
    emoji = emoji.strip()
    return emoji 

@st.cache(persist=True)
def load_data(lang):
    data = pd.read_csv(FILE_PATH)
    data['preprocessed_created_at'] = pd.to_datetime(
        data['preprocessed_created_at'])
    data = data[data["twitter_lang"] == lang]
    sentiments = {
        1: "POS",
        0: "NEG",
    }
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

@st.cache(persist=True)
def get_emojicloud():
    return EmojiCloud(font_path=f"{FONTS_PATH}/Symbola.ttf")

@st.cache(allow_output_mutation=True)
def get_emojis_by_week(data, weeks: int):
    first_week = data["preprocessed_created_at"].dt.week.min()
    rows = data[data["preprocessed_created_at"].dt.week < (weeks + first_week)]
    ans = []
    for i in rows.emoji_list:
        if i != "['']":
            ans.append(clean_emojis(i))
    return ans