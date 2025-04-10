# /agents/market_agent.py

import pandas as pd
import sqlite3
from models.crop_recommender import CropRecommender  # Assuming a basic model exists

class MarketAgent:
    def __init__(self, db_path="farming_data.db", market_data_path="data/market_researcher_dataset.csv"):
        self.db_path = db_path
        self.market_data = self._load_market_data(market_data_path)
        self.crop_recommender = CropRecommender()  # Instantiate the model

    def _load_market_data(self, path):
        """Loads market data from CSV."""
        try:
            return pd.read_csv(path)
        except FileNotFoundError:
            print(f"Error: Market data file not found at {path}")
            return pd.DataFrame()

    def query_database(self, query):
        """Queries the SQLite database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results

    def store_recommendation(self, crop, expected_profit):
        """Stores crop recommendation and expected profit in the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS market_recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                crop TEXT,
                expected_profit REAL,
                timestamp TEXT
            )
        ''')
        cursor.execute('''
            INSERT INTO market_recommendations (crop, expected_profit, timestamp)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        ''', (crop, expected_profit))
        conn.commit()
        conn.close()

    def estimate_profit(self, crop):
        """
        Estimates profit for a given crop by matching 'Product' in market data.
        Returns profit_margin or 'N/A' if not found.
        """
        df = self.market_data.copy()

        if "Product" not in df.columns or "Market_Price_per_ton" not in df.columns or "Competitor_Price_per_ton" not in df.columns:
            return "N/A"

        # Case-insensitive match
        match = df[df["Product"].str.lower() == crop.lower()]

        if not match.empty:
            profit = float(match.iloc[0]["Market_Price_per_ton"] - match.iloc[0]["Competitor_Price_per_ton"])
            return round(profit, 2)
        
        return "N/A"

    def analyze_market_trends(self):
        """Analyzes market trends to identify potentially profitable crops."""
        df = self.market_data.copy()

        if df.empty or 'Market_Price_per_ton' not in df.columns or 'Competitor_Price_per_ton' not in df.columns:
            print("Error: Required columns are missing in market data.")
            return None, None

        # Calculate profit margin
        df['profit_margin'] = df['Market_Price_per_ton'] - df['Competitor_Price_per_ton']

        # Sort and extract the top crop
        sorted_data = df.sort_values(by='profit_margin', ascending=False)
        if not sorted_data.empty:
            top_crop = sorted_data.iloc[0]['Product']  # Column name is Product in the dataset
            expected_profit = sorted_data.iloc[0]['profit_margin']
            return top_crop, expected_profit

        return None, None

    def suggest_profitable_crop(self):
        """Suggests the most profitable crop based on market analysis."""
        crop, profit = self.analyze_market_trends()
        if crop:
            self.store_recommendation(crop, profit)
            return {"suggested_crop": crop, "expected_profit": profit}
        else:
            return {"message": "Could not determine profitable crop."}

if __name__ == '__main__':
    market_agent = MarketAgent()
    profitable_suggestion = market_agent.suggest_profitable_crop()
    print("Profitable Crop Suggestion:", profitable_suggestion)

    # Example: View past recommendations
    # past_recommendations = market_agent.query_database("SELECT * FROM market_recommendations")
    # print("Past Market Recommendations:", past_recommendations)
