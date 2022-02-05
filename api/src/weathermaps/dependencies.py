import os
from dataclasses import dataclass


@dataclass
class OpenWeatherAPI:
    base_url: str
    api_key: str


OPEN_WEATHER_API_CONFIG = OpenWeatherAPI(
    os.getenv("OPEN_WEATHER_ENDPOINT"),
    os.getenv("OPEN_WEATHER_API_KEY"),
)
