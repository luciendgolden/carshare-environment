import logging
import requests

logger = logging.getLogger(__name__)

WEATHER_API_TIMEOUT = 5  # seconds

def get_weather(api_key, lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    try:
        response = requests.get(url, timeout=WEATHER_API_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.Timeout:
        logger.error("Weather API request timed out for lat=%s, lon=%s", lat, lon)
        return {}
    except requests.RequestException as e:
        logger.error("Weather API request failed: %s", e)
        return {}

def evaluate_weather(weather_data):
    weather_condition = weather_data['weather'][0]['main']
    
    if weather_condition in ["Clear", "Clouds"]:
        return "good"
    elif weather_condition in ["Rain", "Snow", "Thunderstorm", "Extreme"]:
        return "bad"
    else:
        # Handle other conditions as needed
        return "moderate"