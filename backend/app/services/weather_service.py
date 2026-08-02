import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


def get_coordinates(location_name):
    """Converts a place name (e.g. 'Tindivanam') into latitude/longitude."""
    response = requests.get(GEOCODING_URL, params={"name": location_name, "count": 1})
    response.raise_for_status()
    data = response.json()

    results = data.get("results")
    if not results:
        return None

    place = results[0]
    return {
        "latitude": place["latitude"],
        "longitude": place["longitude"],
        "resolved_name": f"{place['name']}, {place.get('country', '')}"
    }


def get_forecast(latitude, longitude):
    """Fetches current weather + 5-day forecast for given coordinates."""
    response = requests.get(FORECAST_URL, params={
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m,weather_code",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code",
        "forecast_days": 5,
        "timezone": "auto"
    })
    response.raise_for_status()
    return response.json()