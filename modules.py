from datetime import timezone
import datetime
import pytz
import pgeocode

def get_date_from_days(days):
    dt = datetime.datetime.now(pytz.timezone('EST')) + datetime.timedelta(days=-1 * int(days))
    utc_time = dt.replace(tzinfo=pytz.timezone('EST'))
    date = round(utc_time.timestamp())

    return date

def get_date_now():
    dt = datetime.datetime.now()

    return dt.strftime('%A, %B %d 0:%I:%M%p')

def get_date_from_utc(utc_date):
    return datetime.datetime.fromtimestamp(utc_date).strftime('%A, %B %d %I:%M%p')

def get_coords_from_zip(zipcode):
    """
    provide a five digit zip code and return
    (latidude, longitude)
    """
    nomi = pgeocode.Nominatim('us')
    q = nomi.query_postal_code(str(zipcode))

    lat, lon = q.latitude, q.longitude, 

    return lat, lon

def get_current_forecast(resp):
    description = resp["current"]["weather"][0]["description"]
        
    dt = get_date_from_utc(resp['current']['dt'])
    icon_code = resp["current"]["weather"][0]['icon']
    image_url =  f"http://openweathermap.org/img/wn/{icon_code}@2x.png"

    text = "Current temperature is " + str(resp["current"]["temp"]) + " ℉ with " + description + "."

    return description, dt, icon_code, image_url, text

