# /agents/farmer_agent.py
import pandas as pd
import sqlite3

class FarmerAgent:
    def __init__(self, db_path="farming_data.db"):
        self.db_path = db_path

    def get_farmer_input(self):
        """Simulates getting farmer input."""
        return {
            "soil_type": "loamy",
            "location": "Nanded, Maharashtra",
            "previous_crop": "cotton",
            "water_availability": "medium",
            "preference": "high_profit"
        }

    def process_input(self):
        """Processes farmer input and returns relevant data."""
        return self.get_farmer_input()

    def query_database(self, query):
        """Queries the SQLite database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results

    def store_farm_record(self, data):
        """Stores farm record in the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO farm_records (soil_type, location, previous_crop, water_availability, preference)
            VALUES (?, ?, ?, ?, ?)
        ''', (data["soil_type"], data["location"], data["previous_crop"], data["water_availability"], data["preference"]))
        conn.commit()
        conn.close()

    def collaborate_with_weather_agent(self, location, weather_agent):
        """Collaborates with the WeatherAgent to get forecast."""
        return weather_agent.get_forecast(location)

    def collaborate_with_expert_agent(self, farmer_data, expert_agent):
        """Collaborates with the ExpertAgent for sustainability advice."""
        return expert_agent.get_sustainability_advice(farmer_data)

    def collaborate_with_market_agent(self, market_agent):
        """Collaborates with the MarketAgent for profitable crop suggestions."""
        return market_agent.suggest_profitable_crop()

if __name__ == '__main__':
    farmer_agent = FarmerAgent()
    farmer_data = farmer_agent.process_input()
    print("Farmer Input:", farmer_data)

    # Example of querying the database (assuming database is set up)
    # records = farmer_agent.query_database("SELECT * FROM farm_records")
    # print("Farm Records:", records)