from db import DatabaseHelper
import requests

def get_weather_for_city_api(city,API_KEY,BASE_URL ,db):

    # Setting the parameters for the API request
    params = {
        'q': city,
        'appid': API_KEY,
    }

    url = f"{BASE_URL}?q={city}&appid={API_KEY}"

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        feels_like = data['main']['feels_like']
        print(f"{city}: temperature = {temperature}, Feels Like = {feels_like}")

        db.insert_api_weather_data(city, temperature, feels_like)

    else:
        print(f"Error receiving data for the city {city}. Status code: {response.status_code}")

db = DatabaseHelper()