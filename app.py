from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)
API_KEY = os.getenv("WEATHER_API_KEY", "your_api_key_here")  # replace with your OpenWeatherMap API key

# Predefined list of cities for dropdown
CITIES = ["London", "New York", "Paris", "Tokyo", "Mumbai", "Sydney", "Berlin"]

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

    return render_template("index.html", cities=CITIES, weather=weather_data, selected_city=selected_city)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
