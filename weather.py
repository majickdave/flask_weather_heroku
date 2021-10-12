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

def query_api_historical(days):
    """submit the API query using variables for zip and API_KEY"""

    date = get_date_from_days(days)
    
    try:
        print(HISTORY_API_URL.format(date, API_KEY))
        data = requests.get(HISTORY_API_URL.format(date, API_KEY)).json()
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

    try:
        resp = query_api_zipcode(zipcode)
        description = resp["current"]["weather"][0]["description"]
         
        dt = get_date_from_utc(resp['current']['dt'])
        icon_code = resp["current"]["weather"][0]['icon']
        image_url =  f"http://openweathermap.org/img/wn/{icon_code}@2x.png"

        text = "Current temperature is " + str(resp["current"]["temp"]) + " ℉ with " + description + "." 

        return render_template('current.html', current_forecast=text, date=dt, weather_description=description, 
            the_title=f"Current Weather for {zipcode}", weather_image_url=image_url)
    except:
        text = "There was an error.  Did you include a valid U.S. zip code in the URL?"

        return render_template('404.html', error_message=text)



@app.route('/weather/historical/<days>')
def result_historical(days):
    """
    return a day in history up to 5 days back

    """
    # get the json file from the OpenWeather API
    resp = query_api_historical(days)
    # construct a string using the json data items for temp and
    # description
    try:
        text = resp["name"] + " temperature is " + str(resp["main"]["temp"]) + " degrees Fahrenheit with " + resp["weather"][0]["description"] + "."
    except:
        text = "There was an error.<br>Did you include a valid U.S. zip code in the URL?"
    
    # parsed = json.loads(resp)
    # return json.dumps(parsed, indent=4, sort_keys=True)
    return resp

if __name__ == '__main__':
    app.run(debug=True)