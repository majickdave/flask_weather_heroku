from datetime import timezone
import datetime
import pytz
import pgeocode

def get_date_from_days(days):
    dt = datetime.datetime.now(pytz.timezone('EST')) + datetime.timedelta(days=-1 * int(days))
    utc_time = dt.replace(tzinfo=pytz.timezone('EST'))
    date = round(utc_time.timestamp())

    return date

def get_date_now(date_only=False):
    dt = datetime.datetime.now()

    return dt.strftime('%A, %B %d 0:%I:%M%p')

def get_date_from_utc(utc_date):
    return datetime.datetime.fromtimestamp(utc_date)

def get_coords_from_zip(zipcode):
    """
    provide a five digit zip code and return
    (latidude, longitude)
    """
    nomi = pgeocode.Nominatim('us')
    q = nomi.query_postal_code(str(zipcode))

    lat, lon = q.latitude, q.longitude, 

    return lat, lon

def get_forecast(resp, duration='current'):
    if duration == 'current':
        resp = resp['current']
        icon_size = '2'
    elif resp == 'hourly':
        resp = resp['hourly']
        icon_size = '1'

    description = resp["weather"][0]["description"]
    dt = resp['dt']
    icon_code = resp["weather"][0]['icon']
    text = "Current temperature is " + str(resp["temp"]) + " ℉ with " + description + "."

    image_url =  f"http://openweathermap.org/img/wn/{icon_code}@{icon_size}x.png"

    return description, dt, image_url

def get_icon_url(icon_code, icon_size=1):
    image_url =  f"http://openweathermap.org/img/wn/{icon_code}@{icon_size}x.png"

    return image_url
    

