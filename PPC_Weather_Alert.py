#!/usr/bin/python

from weather import Weather # wrapper for yahoo weather api
import requests
import datetime
import pandas as pd
import numpy as np
import os


# remove max row limit
pd.set_option('display.max_rows', None)

weather = Weather()

# define location variables
NY = weather.lookup_by_location('NewYork')
Boston = weather.lookup_by_location('Boston')
Chicago = weather.lookup_by_location('Chicago')
Dallas = weather.lookup_by_location('Dallas')
Houston = weather.lookup_by_location('Houston')
LA = weather.lookup_by_location('LosAngeles')
SDiego = weather.lookup_by_location('SanDiego')
SanFran = weather.lookup_by_location('SanFrancisco')
Sacramento = weather.lookup_by_location('Sacramento')


cities = [NY, Boston, Chicago, Dallas, Houston, LA, SDiego, SanFran, Sacramento]
cityNames = ["NY", "Boston", "Chicago", "Dallas", "Houston", "LA", "SDiego", "SanFran", "Sacramento"]

# define dictionary, with name:object pairs
dicts = dict(zip(cityNames,cities))

# initiate empty lists to store values
np_cities = []
np_high = []
np_low = []
np_text = []


# iterate over dictionary to obtain weather forecast in each location
def weather_alert():
    for x,y in dicts.items():
        cityF = y.forecast() # declare new variable for the forecast method
        for z in cityF:
            print(str(z['high']),str(z['low']), str(z['text'])) # prints high, low, and description for each location
            np_cities.append(x)
            np_high.append(str(z['high']))
            np_low.append(str(z['low']))
            np_text.append(str(z['text']))
    return


# run function
weather_alert()

# create data frame

raw_data = {
    'city': np_cities,
    'high': np_high,
    'low': np_low,
    'text': np_text
}

df = pd.DataFrame(raw_data, columns=['city', 'high', 'low', 'text']).set_index('city')
df_html = df.to_html # send to html

# set subject
subject = "PPC Weather Alerts" + " " + str(datetime.date.today())

# send email function
def mailgun():
    r = requests.post(
        os.environ['MG_URL'],
        auth=("api", os.environ['MG_API']),
        data={
            "subject": subject,
            "from": "PPC_ALERTS@mail.codyandnick.com",
            "to": "nlafferty@modernize.com",
            "text": df_html,
        }
    )
    return r

# send email
mailgun()