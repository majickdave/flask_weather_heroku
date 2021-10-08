"""a demo Flask app to access an API
   the idea for this example came from:
   https://medium.com/free-code-camp/how-to-build-a-web-app-using-pythons-flask-and-google-app-engine-52b1bb82b221
"""

import requests
import json
from flask import Flask
from datetime import timezone
import datetime
import pytz

app = Flask(__name__)

# this is not a real key
API_KEY = '17afee29d93a1db02dda0f1817e0aca1'

# get weather by U.S. zip code
API_URL = ('https://api.openweathermap.org/data/2.5/onecall?lat=39.40538934466007&lon=-76.70943148008318&exclude=[current, minutely, hourly, alerts]&units=imperial&appid={}')
HISTORY_API_URL = ('https://api.openweathermap.org/data/2.5/onecall/timemachine?lat=39.40538934466007&lon=-76.70943148008318&dt={}&appid={}')



def query_api(days):
    """submit the API query using variables for zip and API_KEY"""

    dt = datetime.datetime.now(pytz.timezone('EST')) + datetime.timedelta(days=-1 * int(days))
    utc_time = dt.replace(tzinfo=pytz.timezone('EST'))
    date = round(utc_time.timestamp())
    
    try:
        print(HISTORY_API_URL.format(date, API_KEY))
        data = requests.get(HISTORY_API_URL.format(date, API_KEY)).json()
    except Exception as exc:
        print(exc)
        data = None
    return data

@app.route('/')
def hello():
    greet = '<h1>Welcome to the topping weather app</h1>'
    content = '<p>Only weather for 8508 topping road</p>'
    link1 = "<p><a href='/weather/1'>Yesterday's weather!</a></p>"
    link2 = "<p><a href='/weather/2'>2 days ago weather!</a></p>"
    link3 = "<p><a href='/weather/3'>3 days ago weather!</a></p>"
    return greet + content + link1 + link2 + link3

@app.route('/weather/<days>')
def result(days):
    """
    options for exclude:
    [current, minutely, hourly, daily, alerts]
    http://127.0.0.1:5000/weather/39.40538934466007:-76.70943148008318:(hourly,%20minutely)
    https://api.openweathermap.org/data/2.5/onecall?lat=39.40538934466007&lon=-76.70943148008318&exclude=[hourly,minutely]&units=imperial&appid=17afee29d93a1db02dda0f1817e0aca1
    """
    # get the json file from the OpenWeather API
    resp = query_api(days)
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