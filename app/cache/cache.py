import json
import os
import requests
from app.utils.city_data_utils import get_required_attributes
from dotenv import load_dotenv


load_dotenv()
WEATHER_API_URL = os.getenv("WEATHER_API_URI")
WEATHER_API_AUTH_KEY = os.getenv("WEATHER_API_AUTH_KEY")


cached_dict = {}

def query_city(city: str):
    if city not in cached_dict:
        return None
    
    return cached_dict[city]

def add_or_update_city(city: str, city_data: dict):
    cached_dict[city] = city_data

def cron_job():
    print('cron_job ran......')
    for city in cached_dict:
        try:
            response = requests.get(f"{WEATHER_API_URL}?q={city}&key={WEATHER_API_AUTH_KEY}")
            response_dict = json.loads(response.text)
            if 'error' not in response_dict:
                city_data = get_required_attributes(response_dict)
                cached_dict[city] = city_data

        except Exception as error:
            print({"error" : str(error)})
