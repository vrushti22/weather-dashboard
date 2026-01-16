from flask import Flask, request
import requests
import os

app = Flask(__name__)
API_KEY = os.getenv("WEATHER_API_KEY", "your_api_key_here")  # replace with your OpenWeatherMap API key

# Predefined list of cities for dropdown
CITIES = ["Ahmedabad", "Rajkot", "Baroda", "Mehsana", "Mumbai", "Anand", "Surat"]

@app.route("/", methods=["GET", "POST"])
def home():
    weather_data = None
    selected_city = None

    if request.method == "POST":
        selected_city = request.form.get("city")
        if selected_city:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={selected_city}&appid={API_KEY}&units=metric"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                weather_data = {
                    "city": selected_city,
                    "temperature": data["main"]["temp"],
                    "humidity": data["main"]["humidity"],
                    "description": data["weather"][0]["description"]
                }
            else:
                weather_data = {"error": "City not found"}

    # Build HTML inline
    html = """
    <html>
    <head>
        <title>Weather Dashboard</title>
        <style>
            body { font-family: Arial; text-align: center; margin-top: 50px; }
            select, button { padding: 10px; font-size: 16px; }
            .weather { margin-top: 20px; font-size: 18px; }
        </style>
    </head>
    <body>
        <h1>Weather Dashboard</h1>
        <form method="POST">
            <label for="city">Select City:</label>
            <select name="city" id="city">
    """

    # Add options dynamically
    for city in CITIES:
        if city == selected_city:
            html += f'<option value="{city}" selected>{city}</option>'
        else:
            html += f'<option value="{city}">{city}</option>'

    html += """
            </select>
            <button type="submit">Get Weather</button>
        </form>
    """

    # Show weather info if available
    if weather_data:
        html += '<div class="weather">'
        if "error" in weather_data:
            html += f'<p style="color:red;">{weather_data["error"]}</p>'
        else:
            html += f'<p><strong>City:</strong> {weather_data["city"]}</p>'
            html += f'<p><strong>Temperature:</strong> {weather_data["temperature"]} °C</p>'
            html += f'<p><strong>Humidity
