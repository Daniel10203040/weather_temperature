from playwright.sync_api import sync_playwright
from weather_report import generate_html_report
from db import DatabaseHelper
import time
import json
import re

def get_weather_by_city_search(city_name, page,db):
    try:
        page.goto("https://www.timeanddate.com/weather/", timeout=60000)

        page.fill('body > div.main-content-div > header > div.fixed > div > form > input', city_name)
        time.sleep(2)
        page.keyboard.press("Enter")

        page.wait_for_selector(f'a:has-text("{city_name}")', timeout=10000)
        page.click(f'a:has-text("{city_name}")')

        page.wait_for_selector(".h2", timeout=10000)
        time.sleep(1)



        temperature = page.query_selector("#qlook > div.h2").inner_text()
        time.sleep(2)
        p_element = page.query_selector('p:has-text("Feels Like")')
        feels_like_text = re.search(r"Feels Like: [\d\s]+°C", p_element.inner_text()).group(0) if p_element else None


        print(f"{city_name}: {temperature}, {feels_like_text}")


        # Convert strings to numbers
        temperature_value = float(temperature.replace('°C', '').strip())
        feels_like_value = float(
            feels_like_text.replace('Feels Like: ', '').replace('°C', '').strip()) if feels_like_text else None

        # Save to DB
        db.insert_web_weather_data(city_name, temperature_value, feels_like_value)

        return {
            "city": city_name,
            "temperature": temperature,
            "feels_like": feels_like_text
        }

    except Exception as e:
        print(f"Error for city {city_name}: {e}")
        return None

# Saving the results to an array
results = []

with open('cities.json', 'r', encoding='utf-8') as file:
    cities = json.load(file)


db = DatabaseHelper()

with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome", headless=False)
    page = browser.new_page()


    for city in cities:
        result = get_weather_by_city_search(city, page, db)
        if result:
            results.append(result)

    browser.close()

# db.view_all_weather_data()
generate_html_report('data.db')
