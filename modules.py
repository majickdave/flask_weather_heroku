from datetime import timezone
import datetime
import pytz
import pgeocode

def get_date_from_days(days):
    dt = datetime.datetime.now(pytz.timezone('EST')) + datetime.timedelta(days=-1 * int(days))
    utc_time = dt.replace(tzinfo=pytz.timezone('EST'))
    date = round(utc_time.timestamp())

    return date

def get_coords_from_zip(zipcode):
    """
    provide a five digit zip code and return
    (latidude, longitude)
    """
    nomi = pgeocode.Nominatim('us')
    q = nomi.query_postal_code(str(zipcode))

    lat, lon = q.latitude, q.longitude, 

    return lat, lon

