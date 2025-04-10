# /models/sustainability_predictor.py
from sklearn.linear_model import LinearRegression
import pandas as pd

class SustainabilityPredictor:
    def __init__(self, data_path="data/farmer_advisor_dataset.csv"):
        self.model = LinearRegression()
        self.data = self._load_data(data_path)
        if not self.data.empty:
            self._train_model()

    def _load_data(self, path):
        """Loads data for training the sustainability predictor."""
        try:
            return pd.read_csv(path) # Assuming relevant features and 'sustainability_indicator' exist
        except FileNotFoundError:
            print(f"Warning: Data file not found at {path} for sustainability predictor.")
            return pd.DataFrame()

    def _train_model(self):
        """Trains the sustainability prediction model."""
        if 'feature1' in self.data.columns and 'feature2' in self.data.columns and 'sustainability_indicator' in self.data.columns:
            X = self.data[['feature1', 'feature2']].apply(lambda col: pd.factorize(col)[0]) # Simple encoding
            y = self.data['sustainability_indicator']
            self.model.fit(X, y)
        else:
            print("Warning: Insufficient columns in data for training sustainability predictor.")

    def predict(self, features):
        """Predicts the sustainability score based on input features."""
        if not self.data.empty and hasattr(self.model, 'coef_'):
            feature_df = pd.DataFrame([features], columns=['feature1', 'feature2'])
            feature_df = feature_df.apply(lambda col: pd.factorize(col, sort=True)[0]) # Ensure same encoding
            return self.model.predict(feature_df)
        else:
            return [0.5] # Default prediction if model not trained

if __name__ == '__main__':
    predictor = SustainabilityPredictor()
    score = predictor.predict(['loamy', 'high'])
    print("Sustainability Score:", score)