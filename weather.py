"""a demo Flask app to access an API
   the idea for this example came from:
   https://medium.com/free-code-camp/how-to-build-a-web-app-using-pythons-flask-and-google-app-engine-52b1bb82b221
"""

import requests
from configparser import ConfigParser
from flask import Flask
from flask import Flask, render_template, redirect
from modules import *
import time
import os

app = Flask(__name__)

if not os.getenv("API_KEY") or not os.getenv("GOOGLE_API_KEY"):
    # obtain keys from .cfg locally from ~./../python
    config = ConfigParser()
    config.read('../../config/keys_config.cfg')
    API_KEY = config.get('openweather', 'api_key')
    AGRO_KEY = config.get('agro', 'api_key')
    GOOGLE_API_KEY = config.get('google', 'geocode_api_key')
else:
    # get key from remote server env
    API_KEY = os.getenv("API_KEY")
    AGRO_KEY = config.get("AGRO_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# get historical and current weather
ONECALL_API_URL = ('https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=&units=imperial&appid={}')
HISTORY_API_URL = ('https://api.openweathermap.org/data/2.5/onecall/timemachine?lat=39.40538934466007&lon=-76.70943148008318&dt={}&units=imperial&appid={}')
PRECIP_API_URL = ('https://api.weatherbit.io/v2.0/history/daily?postal_code=21208&country=US&start_date={}&end_date={}&key={}')

@app.route('/')
def index(zipcode=21208):
    resp, my_city = query_api_zipcode(zipcode)
    precip = query_precip()
    return render_template('index.html', city=my_city, get_date=get_date_from_utc, enumerate=enumerate,
    data=resp, the_title="Dave's weather app", precip=precip,
    round=round, get_wind=get_wind_direction)

@app.route('/weather')
def home_redirect():
    return redirect("/") 

@app.route('/precip')
def get_precip():
    data = query_precip()
    return data

def query_precip(units='in'):
    start = get_date_from_utc(get_date_from_days(3)).strftime('%Y-%m-%d')
    end = get_date_from_utc(get_date_from_days(0)).strftime('%Y-%m-%d')

    try:
        print(PRECIP_API_URL.format(start, end, AGRO_KEY))
        data = requests.get(PRECIP_API_URL.format(start, end, AGRO_KEY)).json()
    except Exception as exc:    
        print(exc)
        data = None

    total_precip = 0

    for day in data['data']:
        total_precip += day['precip']
    
    if units == 'in':
        return total_precip / 25.4

def query_api_historical(days_ago):
    """submit the API query using variables for days and API_KEY"""

    # get date from number of days ago
    date = get_date_from_days(days_ago)
    
    try:
        print(HISTORY_API_URL.format(date, API_KEY))
        data = requests.get(HISTORY_API_URL.format(date, API_KEY)).json()
        data
    except Exception as exc:
        print(exc)
        data = None
    
    return data

def query_api_zipcode(zipcode, query_city=False):
    """submit the API query using variables for zip and API_KEY"""
    
    lat, lon = get_coords_from_zip(zipcode)

    # Google geocode API
    my_city = "Pikesville"
    if query_city:  
        my_city = get_city(lat, lon, GOOGLE_API_KEY) 

    try:
        print(ONECALL_API_URL.format(lat, lon, API_KEY))
        data = requests.get(ONECALL_API_URL.format(lat, lon, API_KEY)).json()
    except Exception as exc:
        print(exc)
        data = None
    return data, my_city


@app.route('/weather/<zipcode>')
def result_zipcode(zipcode):
    """
    options for exclude:
    [current, minutely, hourly, daily, alerts]

    """
    resp = query_api_zipcode(zipcode)

    try:      
        description, dt, image_url = get_forecast(resp, duration='current')
        return render_template('current.html', data=resp, get_date=get_date_from_utc, date=dt, weather_description=description, 
            the_title=f"Current Weather for {zipcode}", weather_image_url=image_url)
    except:
        return render_template('404.html', error_message="something went wrong")



@app.route('/weather/<zipcode>/historical/<days>')
def result_historical(zipcode, days):
    """
    return a day in history up to 5 days back

    """
    # get the json file from the OpenWeather API
    resp = query_api_historical(days)
    # construct a string using the json data items for temp and
    # description
    try:
        return render_template('hourly.html', get_icon=get_icon_url, data=resp, get_date=get_date_from_utc, round=round)
    except Exception as exc:
        return render_template('404.html', error_message=exc)


if __name__ == '__main__':
    app.run(debug=True)