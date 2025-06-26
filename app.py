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
    openweather_icon = data["weather"][0]["icon"]
    accuweather_icon, accuweather_text = get_icon_and_text(openweather_icon)
    daylight = "True" if openweather_icon.endswith("d") else "False"

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
<weathertext>{accuweather_text}</weathertext>
<weathericon>{accuweather_icon}</weathericon>
</currentconditions>
</weather>
"""
    return Response(xml, mimetype='application/xml')

def get_icon_and_text(openweather_icon):
    mapping = {
        "01d": ("1", "Sunny"),
        "01n": ("33", "Clear"),
        "02d": ("2", "Mostly Sunny"),
        "02n": ("34", "Mostly Clear"),
        "03d": ("3", "Partly Sunny"),
        "03n": ("35", "Partly Cloudy"),
        "04d": ("7", "Cloudy"),
        "04n": ("38", "Mostly Cloudy"),
        "09d": ("12", "Showers"),
        "09n": ("40", "Mostly Cloudy with Showers"),
        "10d": ("14", "Partly Sunny with Showers"),
        "10n": ("39", "Partly Cloudy with Showers"),
        "11d": ("15", "Thunder Storms"),
        "11n": ("41", "Partly Cloudy with Thunder Storms"),
        "13d": ("22", "Snow"),
        "13n": ("44", "Mostly Cloudy with Snow"),
        "50d": ("11", "Fog"),
        "50n": ("11", "Fog")
    }
    return mapping.get(openweather_icon, ("7", "Cloudy"))

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
