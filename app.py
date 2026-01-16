from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)
API_KEY = os.getenv("WEATHER_API_KEY", "your_api_key_here")  # replace with your OpenWeatherMap API key

@app.route("/")
def home():
    return jsonify({"status": "Weather app running"})

@app.route("/weather/<city>")
def weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return jsonify({
            "city": city,
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"]
        })
    else:
        return jsonify({"error": "City not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
