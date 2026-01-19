from flask import Flask, request
import requests
import os
from prometheus_client import (
    Counter,
    Histogram,
    generate_latest,
    CONTENT_TYPE_LATEST
)

app = Flask(__name__)

# =========================
# Configuration
# =========================
API_KEY = os.getenv("WEATHER_API_KEY")  # MUST be set as env variable
CITIES = ["London", "New York", "Paris", "Tokyo", "Mumbai", "Sydney", "Berlin"]

# =========================
# Prometheus Metrics
# =========================
REQUEST_COUNT = Counter(
    "weather_app_requests_total",
    "Total number of HTTP requests"
)

WEATHER_API_COUNT = Counter(
    "weather_api_requests_total",
    "Total calls made to OpenWeather API"
)

REQUEST_LATENCY = Histogram(
    "weather_app_request_latency_seconds",
    "Latency of HTTP requests in seconds"
)

# =========================
# Routes
# =========================
@app.route("/", methods=["GET", "POST"])
@REQUEST_LATENCY.time()
def home():
    REQUEST_COUNT.inc()

    weather_data = None
    selected_city = None

    if request.method == "POST":
        selected_city = request.form.get("city")

        if selected_city and API_KEY:
            WEATHER_API_COUNT.inc()
            url = (
                "https://api.openweathermap.org/data/2.5/weather"
                f"?q={selected_city}&appid={API_KEY}&units=metric"
            )
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
                weather_data = {
                    "error": f"API Error {response.status_code}"
                }
        else:
            weather_data = {
                "error": "API key not configured"
            }

    # =========================
    # Inline HTML
    # =========================
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
            <label>Select City:</label>
            <select name="city">
    """

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

    if weather_data:
        html += '<div class="weather">'
        if "error" in weather_data:
            html += f'<p style="color:red;">{weather_data["error"]}</p>'
        else:
            html += f"<p><b>City:</b> {weather_data['city']}</p>"
            html += f"<p><b>Temperature:</b> {weather_data['temperature']} °C</p>"
            html += f"<p><b>Humidity:</b> {weather_data['humidity']}%</p>"
            html += f"<p><b>Description:</b> {weather_data['description']}</p>"
        html += "</div>"

    html += """
        <p style="margin-top:40px; font-size:14px;">
            Metrics available at <b>/metrics</b>
        </p>
    </body>
    </html>
    """

    return html


# =========================
# Prometheus Metrics Endpoint
# =========================
@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


# =========================
# App Start
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
