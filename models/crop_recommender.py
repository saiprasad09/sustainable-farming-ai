# /models/crop_recommender.py

from sklearn.tree import DecisionTreeClassifier
import pandas as pd

class CropRecommender:
    def __init__(self, data_path="data/farmer_advisor_dataset.csv"):
        self.model = DecisionTreeClassifier()
        self.trained = False
        self.data = self._load_data(data_path)
        if not self.data.empty:
            self._train_model()

    def _load_data(self, path):
        """Loads data for training the crop recommender."""
        try:
            return pd.read_csv(path)
        except FileNotFoundError:
            print(f"Warning: Data file not found at {path} for crop recommender.")
            return pd.DataFrame()

    def _train_model(self):
        """Trains the crop recommendation model."""
        required_cols = {'Soil_pH', 'Soil_Moisture', 'Temperature_C', 'Rainfall_mm', 'Crop_Type'}
        if required_cols.issubset(self.data.columns):
            X = self.data[['Soil_pH', 'Soil_Moisture', 'Temperature_C', 'Rainfall_mm']]
            y = self.data['Crop_Type']
            self.model.fit(X, y)
            self.trained = True
        else:
            print("Warning: Required columns missing for training crop recommender.")

    def recommend(self, soil_pH, moisture, temperature, rainfall):
        """Predicts crop using ML model, fallback to rules if model isn't trained."""
        if self.trained:
            input_df = pd.DataFrame([{
                'Soil_pH': soil_pH,
                'Soil_Moisture': moisture,
                'Temperature_C': temperature,
                'Rainfall_mm': rainfall
            }])
            prediction = self.model.predict(input_df)
            return prediction[0]
        else:
            # Fallback: Rule-based recommendation
            if soil_pH < 6.0:
                return "Soybean"
            elif rainfall > 150:
                return "Rice"
            elif temperature > 30:
                return "Corn"
            else:
                return "Wheat"

if __name__ == '__main__':
    recommender = CropRecommender()
    crop = recommender.recommend(soil_pH=6.5, moisture=30, temperature=28, rainfall=120)
    print("Recommended Crop:", crop)
