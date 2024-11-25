import os

class Config:
    OPEN_WEATHER_API_KEY = os.getenv('OPEN_WEATHER_API_KEY', 'your-local-key')