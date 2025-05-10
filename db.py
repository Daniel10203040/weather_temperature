import sqlite3


class DatabaseHelper:
    def __init__(self, db_name="data.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS weather_data (
                    city TEXT PRIMARY KEY,
                    temperature_web REAL,
                    feels_like_web REAL,
                    temperature_api REAL,
                    feels_like_api REAL
                )
            ''')

    def insert_web_weather_data(self, city, temperature_web, feels_like_web):
        with self.conn:
            # print(f"Inserting Web data for city: {city}")
            self.conn.execute('''
                  INSERT INTO weather_data (city, temperature_web, feels_like_web)
                  VALUES (?, ?, ?)
                  ON CONFLICT(city) DO UPDATE SET
                      temperature_web = excluded.temperature_web,
                      feels_like_web = excluded.feels_like_web
              ''', (city, temperature_web, feels_like_web))

    def insert_api_weather_data(self, city, temperature_api, feels_like_api):
        with self.conn:

            # Insert the data for API into the weather_data table
            self.conn.execute('''
                INSERT OR REPLACE INTO weather_data (
                    city,
                    temperature_api,
                    feels_like_api
                ) VALUES (?, ?, ?)
            ''', (
                city,
                temperature_api,
                feels_like_api
            ))


    def view_all_weather_data(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM weather_data')
        rows = cursor.fetchall()
        for row in rows:
            print(row)
