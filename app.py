from flask import Flask, Response
import requests

app = Flask(__name__)

API_KEY = "8c59d438f271df58f85c89b870d0d973"  # Replace with your real OpenWeatherMap API key
CITY = "Manchester,GB"
CITY_ID = "329260"
URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

@app.route("/weather.xml")
def weather():
    data = requests.get(URL).json()

    temperature = int(data["main"]["temp"])
    realfeel = int(data["main"]["feels_like"])
    humidity = f'{data["main"]["humidity"]}%'
    weather_text = data["weather"][0]["description"].title()
    weather_icon = get_icon_code(data["weather"][0]["icon"])
    daylight = "True" if data["weather"][0]["icon"].endswith("d") else "False"

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<weather>
<local>
<city>Manchester</city>
<country code="GB">United Kingdom</country>
<cityId>{CITY_ID}</cityId>
</local>
<currentconditions daylight="{daylight}">
<observationtime>Live</observationtime>
<temperature>{temperature}</temperature>
<realfeel>{realfeel}</realfeel>
<unit>C</unit>
<humidity>{humidity}</humidity>
<weathertext>{weather_text}</weathertext>
<weathericon>{weather_icon}</weathericon>
</currentconditions>
</weather>
"""
    return Response(xml, mimetype='application/xml')

def get_icon_code(openweather_icon):
    mapping = {
        "01d": "1", "01n": "33",
        "02d": "2", "02n": "34",
        "03d": "3", "03n": "35",
        "04d": "7", "04n": "38",
        "09d": "12", "09n": "40",
        "10d": "14", "10n": "39",
        "11d": "15", "11n": "41",
        "13d": "22", "13n": "44",
        "50d": "11", "50n": "11"
    }
    return mapping.get(openweather_icon, "7")  # default: Cloudy

if __name__ == "__main__":
    app.run
