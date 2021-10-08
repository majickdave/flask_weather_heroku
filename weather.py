"""a demo Flask app to access an API
   the idea for this example came from:
   https://medium.com/free-code-camp/how-to-build-a-web-app-using-pythons-flask-and-google-app-engine-52b1bb82b221
"""

import requests
import json
from flask import Flask
app = Flask(__name__)

# this is not a real key
API_KEY = '17afee29d93a1db02dda0f1817e0aca1'

# get weather by U.S. zip code
API_URL = ('https://api.openweathermap.org/data/2.5/onecall?lat=39.40538934466007&lon=-76.70943148008318&exclude=(hourly,%20minutely)&units=imperial&appid={}')

def query_api():
    """submit the API query using variables for zip and API_KEY"""
    try:
        # print(API_URL.format(zip, API_KEY))
        data = requests.get(API_URL.format(API_KEY)).json()
    except Exception as exc:
        print(exc)
        data = None
    return data
    
@app.route('/weather')
def result():
    """
    options for exclude:
    [current, minutely, hourly, daily, alerts]
    http://127.0.0.1:5000/weather/39.40538934466007:-76.70943148008318:(hourly,%20minutely)
    """
    # get the json file from the OpenWeather API
    resp = query_api()
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