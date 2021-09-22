import pandas as pd
from pysentimiento import SentimentAnalyzer, EmotionAnalyzer

sentiment_analyzer_es = SentimentAnalyzer(lang="es")
emotion_analyzer_es = EmotionAnalyzer(lang="es")

# Read data
data = pd.read_csv('Corrected_Final_All.csv')
# data = pd.read_csv('final_all.csv', usecols=['full_text', 'lang', 'preprocessed_data', 'preprocessed_data_without_hashtags'])


# Select spanish tweets
spanish_df = data[data['lang'] == 'es']

# Generate new feature with sentiment and emotion
spanish_df['full_text_sentiment'] = spanish_df['full_text'].apply(lambda tweet: sentiment_analyzer_es.predict(tweet).output)
spanish_df['full_text_emotion'] = spanish_df['full_text'].apply(lambda tweet: emotion_analyzer_es.predict(tweet).output)


# Save the data
spanish_df.to_csv('sentiment_spanish_df.csv')