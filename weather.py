"""a demo Flask app to access an API
   the idea for this example came from:
   https://medium.com/free-code-camp/how-to-build-a-web-app-using-pythons-flask-and-google-app-engine-52b1bb82b221
"""

import requests
import json
from flask import Flask
from flask import Flask, render_template
from modules import *

app = Flask(__name__)

# this is not a real key
API_KEY = '17afee29d93a1db02dda0f1817e0aca1'

# get weather by U.S. zip code
ONECALL_API_URL = ('https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=daily,hourly,minutely,alerts&units=imperial&appid={}')
HISTORY_API_URL = ('https://api.openweathermap.org/data/2.5/onecall/timemachine?lat=39.40538934466007&lon=-76.70943148008318&dt={}&units=imperial&appid={}')


@app.route('/')
def index():
    return render_template('index.html', days=list(range(1,6)), the_title="Dave's weather app")

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

def query_api_zipcode(zipcode):
    """submit the API query using variables for zip and API_KEY"""
    
    lat, lon = get_coords_from_zip(zipcode)
    try:
        # print(HISTORY_API_URL.format(date, API_KEY))
        data = requests.get(ONECALL_API_URL.format(lat, lon, API_KEY)).json()
    except Exception as exc:
        print(exc)
        data = None
    return data


@app.route('/weather/<zipcode>')
def result_zipcode(zipcode):
    """
    options for exclude:
    [current, minutely, hourly, daily, alerts]

    """
    dt = get_date_now()
    resp = query_api_zipcode(zipcode)
    try:      
        description, dt, icon_code, image_url, text = get_current_forecast(resp)

        return render_template('current.html', current_forecast=text, date=dt, weather_description=description, 
            the_title=f"Current Weather for {zipcode}", weather_image_url=image_url)
    except:
        text = "There was an error.  Did you include a valid U.S. zip code in the URL?"

        return render_template('404.html', error_message=text)



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
        description, dt, icon_code, image_url, text = get_current_forecast(resp)
        return render_template('current.html', current_forecast=text, date=dt, weather_description=description, 
            the_title=f"Current Weather for {zipcode}", weather_image_url=image_url)
    except:
        text = "There was an error.  Did you use days <= 5?"

        return render_template('404.html', error_message=text)
    
    # parsed = json.loads(resp)
    # return json.dumps(parsed, indent=4, sort_keys=True)
    return resp

if __name__ == '__main__':
    app.run(debug=True)