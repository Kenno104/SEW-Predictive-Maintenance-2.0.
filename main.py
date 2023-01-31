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
  st.text('Product ID: ' + df['productID'][0])

with col2:
  st.subheader("Last Repair Date:")
  st.text(df['repair_dates'][len(df) - 1])
  
with col3:
  st.subheader("Mean time between failures:")
  st.subheader(f":blue[{avg_reliability} Days]")

col4, col5, col6 = st.columns(3)

with col4:
  st.subheader('Customer: ' + df['customer'][0])
  st.text(df['address'][0])

with col5:
  st.subheader("No. Repairs To Date:")
  st.subheader(len(df['repair_dates']))
  
with col6:
  st.subheader('Estimated Next Repair Date:')
  st.subheader(f":blue[{df['repair_dates'][len(df) - 1] + timedelta(days=avg_reliability)}]")

#SECTION 2: Graph
fig, ax = plt.subplots()
for i in range(len(df) - 1):
  start_date = df.iloc[i]['repair_dates']
  end_date = df.iloc[i + 1]['repair_dates']
  x = [start_date, end_date]
  y = [0, (end_date - start_date).days]
  ax.plot(x, y, '-b')
  ax.vlines(end_date,
            0, (end_date - start_date).days,
            color='black',
            linestyle='dotted',
            alpha=0.4)

# Draw the last line to today's date
x = [df.iloc[-1]['repair_dates'], datetime_object]
y = [0, (datetime_object - df.iloc[-1]['repair_dates']).days]
ax.plot(x, y, '-b', label='Current lifetime')


ax.axhline(y=avg_reliability,
           color='orange',
           linestyle='--',
           label='Expected Lifetime',
           linewidth=1)

# Set the x-axis to display the dates
# ax.set_xticks(df['dates'].append(pd.Series(now))) # deprecated expression
ax.set_xticks(pd.concat([df['repair_dates'], pd.Series(datetime_object)]))
ax.xaxis.set_major_formatter(
  plt.FixedFormatter(df['repair_dates'].dt.strftime("%d-%m-%Y")))
ax.xaxis.set_tick_params(rotation=45)

plt.legend()
st.pyplot(fig)

#SECTION 3: Alerts & Actions

col7, col8= st.columns(2)

with col7:
  st.header(':red[Live Alerts]')
  st.subheader('Currently: All Systems :green[Green]')
              
with col8:
  url ='https://www.seweurodrive.com/contact_us/contact_us.html'
  
  st.markdown(f'''<a href={url}><button style="background-color:Blue;">Schedule Maintenance Call</button></a>
''',
unsafe_allow_html=True)