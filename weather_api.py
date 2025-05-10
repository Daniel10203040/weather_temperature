import requests
from functions import get_weather_for_city_api
from weather_report import generate_html_report
import configparser
import json
from db import DatabaseHelper

config = configparser.ConfigParser()
config.read('config.ini')
db = DatabaseHelper()

API_KEY = config['openweathermap']['API_KEY']
BASE_URL = config['openweathermap']['BASE_URL']

# Reading the list of cities from a JSON file
with open('cities.json', 'r') as file:
    cities = json.load(file)


#  A loop that will send an API call for each city
for city in cities:
    get_weather_for_city_api(city,API_KEY,BASE_URL,db)

# After all requests, display all data from the DB
# db.view_all_weather_data()
generate_html_report('data.db')