

import pandas as pd
import streamlit as st
from utils.emojis import EmojiCloud

FILE_PATH = "src/data/task-5-visualization/Corrected_final_all_with_sentiment.csv"
FONTS_PATH = "src/tasks/task-5-visualization/dashboards/utils/fonts"


def clean_emojis(emoji):
    emoji = emoji.replace("[", "")
    emoji = emoji.replace("]", "")
    emoji = emoji.replace("'", "")
    emoji = emoji.strip()
    return emoji


@st.cache(persist=True)
def load_data(lang, start_date, end_date):
    data = pd.read_csv(FILE_PATH)
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
