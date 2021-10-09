### Streamlit dashboard for event timeline


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import numpy as np
import datetime
import streamlit as st

event_df = pd.read_csv('event_df.csv')
high_event_df = pd.read_csv('high_event_df.csv')

choice = st.selectbox('Select your preference: ', ['Time Range', 'Singular Date'])

if choice == 'Singular Date':
    date = datetime.datetime.strptime('2021-04-28', '%Y-%m-%d')
    start_date = st.date_input('Input start date: ', date)
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

    start_date = st.date_input('Input start date: ', dates)
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
                    
    