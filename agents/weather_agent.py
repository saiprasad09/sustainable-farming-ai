# /agents/weather_agent.py

import sqlite3
import random
from datetime import datetime

class WeatherAgent:
    def __init__(self, db_path="farming_data.db"):
        self.db_path = db_path
        self._ensure_table_exists()

    def _ensure_table_exists(self):
        """Creates the weather_forecasts table if it doesn't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weather_forecasts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                location TEXT,
                forecast_date TEXT,
                temperature REAL,
                rainfall REAL,
                humidity REAL
            )
        ''')
        conn.commit()
        conn.close()

    def query_database(self, query):
        """Queries the SQLite database and returns the result."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results

    def store_weather_data(self, location, forecast):
        """Stores a weather forecast in the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO weather_forecasts (location, forecast_date, temperature, rainfall, humidity)
            VALUES (?, ?, ?, ?, ?)
        ''', (location, datetime.now().date(), forecast['temperature'], forecast['rainfall'], forecast['humidity']))
        conn.commit()
        conn.close()

    def get_forecast(self, location):
        """Returns a mock weather forecast for a given location."""
        supported_locations = ["Nanded", "Aurangabad", "Pune"]
        if any(city in location for city in supported_locations):
            forecast = {
                "temperature": round(random.uniform(28, 38), 1),
                "rainfall": round(random.uniform(0, 30), 1),
                "humidity": round(random.uniform(40, 85), 1)
            }
            self.store_weather_data(location, forecast)
            return forecast
        else:
            return {
                "error": True,
                "message": f"⚠️ Forecast not available for '{location}'. Try: Nanded, Aurangabad, Pune."
            }

if __name__ == '__main__':
    weather_agent = WeatherAgent()
    forecast = weather_agent.get_forecast("Nanded, Maharashtra")
    print("Forecast:", forecast)

    unknown = weather_agent.get_forecast("Unknown Location")
    print("Unknown Location Forecast:", unknown)

    # Optional: View past forecasts
    # results = weather_agent.query_database("SELECT * FROM weather_forecasts")
    # print("Past Forecasts:", results)
