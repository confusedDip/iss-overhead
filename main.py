import requests
from datetime import datetime

# Define my location
MY_LAT = 45.53790744833541
MY_LONG = -122.90789975659347

# Make the ISS location API call
response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

# Retrieve the ISS position
iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])


# Helper method to check if the ISS position is within +5 or -5 degrees of my position.
def isNear(iss_position, my_position):
    """

    :param iss_position: The current latitude and longitude of ISS
    :param my_position: My current latitute and longitude
    :return: True, if ISS position is within +5 or -5 degrees of my position
                False, otherwise
    """
    margin = 5

    iss_lat, iss_long = iss_position
    my_lat, my_long = my_position

    return my_lat - margin <= iss_lat <= my_lat + margin and my_long - margin <= iss_long <= my_long + margin


# Helper method to check if it is dark now
def isDark(current, sunrise_t, sunset_t):
    return not (sunrise_t <= current.hour <= sunset_t)


# Make the API Call
response = requests.get(
    "https://api.sunrise-sunset.org/json",
    params={
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
)
response.raise_for_status()
data = response.json()

# Get the required fields
sunrise = data["results"]["sunrise"]
sunset = data["results"]["sunset"]

# Get the times
sunrise_time = int(sunrise.split('T')[1][:2])
sunset_time = int(sunset.split('T')[1][:2])

# Convert from UTC to Local Time
time_offset = -8
sunset_time += time_offset
sunrise_time += time_offset

# Get the current time
current_datetime = datetime.now()
current_time = current_datetime.time()

# Final Check!
if isNear(iss_position=(iss_latitude, iss_longitude), my_position=(MY_LAT, MY_LONG)) \
        and isDark(current_time, sunrise_time, sunset_time):
    print("Look Up!")
else:
    print("Sorry, it's day time or/and the ISS is far away!")
