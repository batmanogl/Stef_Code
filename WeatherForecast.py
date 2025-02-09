from PIL import Image
from io import BytesIO
from datetime import datetime
import pytz
import requests
from pprint import pprint

API_Key = "db56094bb182ac397d8736c695755457"
continent = input("Enter the name of the CONTINENT to set your local time zone:")
city = input("Enter the valid CITY name to accurately set the local time zone:")
city_forecast = input("Enter the name of the CITY for which you want to receive a weather forecast:")
cont_city = continent + "/" + city

# Set the timezone
try:
    local_tz = pytz.timezone(cont_city)
except pytz.UnknownTimeZoneError:
    print("Invalid timezone. Please enter a correct continent/city format (e.g., 'Europe/Athens').")
    exit()

print("\nThe temperature is in Celsius units.\n")

base_url = "https://api.openweathermap.org/data/2.5/weather?appid="+API_Key+"&lang=el&units=metric&q="+city_forecast
#base_url = "https://api.openweathermap.org/data/2.5/forecast/hourly?appid="+API_Key+"&q="+city
#base_url = "https://api.openweathermap.org/data/2.5/weather?appid=db56094bb182ac397d8736c695755457&q=London&lang=el"
#base_url = "https://pro.openweathermap.org/data/2.5/forecast/hourly?lat=57&lon=-2.15db56094bb182ac397d8736c695755457&cnt=3"

weather_data = requests.get(base_url).json()
pprint(weather_data)

# Get weather data

# Extract sunrise and sunset times (Unix timestamps)
if "sys" in weather_data:
    sunrise_utc = weather_data["sys"]["sunrise"]
    sunset_utc = weather_data["sys"]["sunset"]

    # Extract icon code safely
    weather_icon_code = weather_data["weather"][0].get("icon", "")

    # Convert to local timezone
    sunrise_local = datetime.fromtimestamp(sunrise_utc, pytz.utc).astimezone(local_tz)
    sunset_local = datetime.fromtimestamp(sunset_utc, pytz.utc).astimezone(local_tz)

    # Construct the weather icon URL
    if weather_icon_code:
        icon_url = f"https://openweathermap.org/img/wn/{weather_icon_code}@2x.png"
    else:
        icon_url = "No icon available"

    # Print results
    print("\n🌅 Sunrise (Local Time):", sunrise_local.strftime("%Y-%m-%d %H:%M:%S %Z"))
    print("🌇 Sunset (Local Time):", sunset_local.strftime("%Y-%m-%d %H:%M:%S %Z"))
    print(f"🌤 Weather Icon: {icon_url}")
else:
    print("Error: Could not retrieve sunrise and sunset times. Check your city name and API key.")

if weather_icon_code:
    response = requests.get(icon_url)
    img = Image.open(BytesIO(response.content))
    img.show()
