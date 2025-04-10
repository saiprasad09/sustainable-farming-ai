# /agents/expert_agent.py

import pandas as pd
import sqlite3
from models.sustainability_predictor import SustainabilityPredictor  # Assuming a basic model exists

class ExpertAgent:
    def __init__(self, db_path="farming_data.db", advisor_data_path="data/farmer_advisor_dataset.csv"):
        self.db_path = db_path
        self.advisor_data = self._load_advisor_data(advisor_data_path)
        self.sustainability_predictor = SustainabilityPredictor()  # Instantiate the model
        self._ensure_table_exists()  # Ensure table is created

    def _ensure_table_exists(self):
        """Creates the sustainability_scores table if it doesn't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sustainability_scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                soil_type TEXT,
                location TEXT,
                previous_crop TEXT,
                water_availability TEXT,
                score REAL,
                timestamp TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def _load_advisor_data(self, path):
        """Loads farmer advisor data from CSV."""
        try:
            return pd.read_csv(path)
        except FileNotFoundError:
            print(f"Error: Farmer advisor data file not found at {path}")
            return pd.DataFrame()

    def query_database(self, query):
        """Queries the SQLite database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results

    def store_sustainability_score(self, farm_data, score):
        """Stores the calculated sustainability score in the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO sustainability_scores (soil_type, location, previous_crop, water_availability, score, timestamp)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (
            farm_data.get('soil_type', 'unknown'),
            farm_data.get('location', 'unspecified'),
            farm_data.get('previous_crop', 'unknown'),
            farm_data.get('water_availability', 'unknown'),
            score
        ))
        conn.commit()
        conn.close()

    def calculate_sustainability_score(self, farm_data):
        """Estimates a sustainability score based on farm data."""
        # Simple placeholder logic - replace with actual model prediction
        features = [
            1 if farm_data['soil_type'] == 'loamy' else 0,
            1 if farm_data['water_availability'] == 'high' else (0.5 if farm_data['water_availability'] == 'medium' else 0),
            1 if farm_data['previous_crop'] in ['legume', 'cover_crop'] else 0
        ]
        # Predict using the sustainability predictor model
        score = self.sustainability_predictor.predict([features])[0]
        self.store_sustainability_score(farm_data, score)
        return score

    def get_sustainability_advice(self, farm_data):
        """Provides sustainability advice based on the calculated score."""
        score = self.calculate_sustainability_score(farm_data)
        if score > 0.7:
            return {"advice": "✅ High sustainability. Consider optimizing resource usage even further."}
        elif 0.4 <= score <= 0.7:
            return {"advice": "⚠️ Medium sustainability. Adopt better crop rotation, irrigation, and organic practices."}
        else:
            return {"advice": "❌ Low sustainability. Immediate action required to prevent environmental degradation."}

if __name__ == '__main__':
    expert_agent = ExpertAgent()
    farmer_data = {
        "soil_type": "sandy",
        "location": "Nanded, Maharashtra",
        "previous_crop": "maize",
        "water_availability": "low"
    }
    advice = expert_agent.get_sustainability_advice(farmer_data)
    print("Sustainability Advice:", advice)

    # Example of querying past sustainability scores
    # past_scores = expert_agent.query_database("SELECT * FROM sustainability_scores WHERE location = 'Nanded, Maharashtra'")
    # print("Past Sustainability Scores:", past_scores)
