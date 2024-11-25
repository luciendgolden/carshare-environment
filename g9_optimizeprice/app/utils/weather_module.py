import requests

def get_weather(api_key, lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    print(f"Fetching weather data from {url}")
    response = requests.get(url)
    return response.json()

def evaluate_weather(weather_data):
    weather_condition = weather_data['weather'][0]['main']
    
    if weather_condition in ["Clear", "Clouds"]:
        return "good"
    elif weather_condition in ["Rain", "Snow", "Thunderstorm", "Extreme"]:
        return "bad"
    else:
        # Handle other conditions as needed
        return "moderate"