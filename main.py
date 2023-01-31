import streamlit as st  # web development
import pandas as pd  # read csv, df manipulation
import numpy as np
import time  # to simulate a real time data, time loop
from datetime import datetime, timedelta
from PIL import Image
import matplotlib.pyplot as plt

#Page Configuration
st.set_page_config(page_title='Real-Time Data Science Dashboard',
                   page_icon='✅',
                   layout='wide')


#FUNCTIONS
def convert_to_string(delta):
  days = delta.days
  hours, remainder = divmod(delta.seconds, 3600)
  minutes, seconds = divmod(remainder, 60)
  return '{} days {:02}:{:02}:{:02}'.format(days, hours, minutes, seconds)


def convert_to_days(time_string):
  parts = time_string.split(' ')
  days = int(parts[0].strip().strip('days'))
  delta = timedelta(days=days)
  return delta.days


##################

# read in csv
df = pd.read_csv("individ_testdata.csv")

# Convert the dates to datetime objects
df['repair_dates'] = pd.to_datetime(df['repair_dates'], format='%d/%m/%Y')
df['diffs'] = 0

#Find difference (days) between repair dates and convert to integers
for i in range(0, len(df) - 1):
  df['diffs'][i] = abs(df['repair_dates'][i] - df['repair_dates'][i + 1])
  df['diffs'][i] = convert_to_string(df['diffs'][i])
  df['diffs'][i] = convert_to_days(df['diffs'][i])

#Find difference (days) between Today's date and the last repair date. Put this value in the final row for 'diffs':

#Get Today's date as a DateTime object
today = datetime.now()
formatted_date = today.strftime("%Y-%m-%d")
datetime_object = datetime.strptime(formatted_date, "%Y-%m-%d")
#Insert difference (days) in final row of 'diffs'
df['diffs'][len(df) - 1] = abs(df['repair_dates'][len(df) - 1] -
                               datetime_object)
df['diffs'][len(df) - 1] = convert_to_string(df['diffs'][len(df) - 1])
df['diffs'][len(df) - 1] = convert_to_days(df['diffs'][len(df) - 1])

#Find average time between repair dates
#NOTE: The avg_reliability is the mean of the 'diffs', not including the final entry, as this represents the days since the last repair
avg_reliability = int(round(np.mean(df['diffs'][0:-1].dropna()), 0))
#Gets time since last repair (last entry in 'diffs' column)
time_since = int(df['diffs'][len(df) - 1])

col1, col2, col3 = st.columns(3)

with col1:
  st.subheader(df['type'][0])
  st.subheader(df['productID'][0])
  
  st.subheader(df['customer'][0])
  st.text(df['address'][0])

with col2:
  st.subheader("Last Repair")
  st.subheader(df['repair_dates'][len(df) - 1])

  st.subheader("Repairs To Date:")
  st.subheader(len(df['repair_dates']))
  
with col3:
  st.subheader("Mean time between failures")
  st.subheader(avg_reliability)

  st.subheader('Estimated Next Repair')
  # st.subheader(df['repair_dates'][len(df) - 1] + avg_reliability)
