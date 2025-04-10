# app.py
import streamlit as st
from agents.farmer_agent import FarmerAgent
from models.crop_recommender import CropRecommender
from models.sustainability_predictor import SustainabilityPredictor
from agents.market_agent import MarketAgent
from agents.weather_agent import WeatherAgent
from agents.expert_agent import ExpertAgent

# MUST BE THE FIRST STREAMLIT COMMAND
st.set_page_config(page_title="Sustainable Farming Advisor", layout="centered")

st.title("🌾 Sustainable Farming AI Advisor")

# Instantiate agents and models
farmer_agent = FarmerAgent()
crop_recommender = CropRecommender()
sustainability_predictor = SustainabilityPredictor()
market_agent = MarketAgent()
weather_agent = WeatherAgent()
expert_agent = ExpertAgent()

# Input form for user (farmer)
with st.form("farmer_input_form"):
    st.subheader("Enter Farm Information:")
    soil_type = st.selectbox("Soil Type", ["loamy", "sandy", "clay"])
    water_availability = st.selectbox("Water Availability", ["high", "medium", "low"])
    location = st.text_input("Location", value="Nanded, Maharashtra")
    previous_crop = st.text_input("Previous Crop", value="cotton")
    preference = st.selectbox("Preference", ["high_profit", "sustainability"])
    
    # Add missing parameters for recommendation
    soil_pH = st.number_input("Soil pH", value=6.5)
    moisture = st.number_input("Soil Moisture (%)", value=30.0)
    temperature = st.number_input("Temperature (°C)", value=28.0)
    rainfall = st.number_input("Rainfall (mm)", value=140.0)
    
    submitted = st.form_submit_button("Get Recommendation")

# When submitted, process inputs and get recommendations
if submitted:
    farmer_input = {
        "soil_type": soil_type,
        "water_availability": water_availability,
        "location": location,
        "previous_crop": previous_crop,
        "preference": preference
    }

    # Recommend crop based on soil, weather, etc.
    recommendation_features = {
        "soil_pH": soil_pH,
        "moisture": moisture,
        "temperature": temperature,
        "rainfall": rainfall
    }

    recommended_crop = crop_recommender.recommend(**recommendation_features)
    
    st.success("✅ Recommendation Complete!")
    st.write(f"**Recommended Crop:** {recommended_crop}")

    # Estimate sustainability score
    sustainability_features = {
        "soil_type": soil_type,
        "water_availability": water_availability,
        "previous_crop": previous_crop
    }

    sustainability_score = sustainability_predictor.predict([list(sustainability_features.values())])[0]
    st.write(f"**Estimated Sustainability Score:** {sustainability_score:.2f}")

    # Market estimate
    profit_estimate = market_agent.estimate_profit(recommended_crop)
    st.write(f"**Profit Estimate (from Market):** ₹{profit_estimate} per unit")

    # Weather
    weather_forecast = weather_agent.get_forecast(location)
    st.subheader("Weather Forecast:")
    st.write(weather_forecast)

    # Expert advice
    expert_advice = expert_agent.get_sustainability_advice(farmer_input)
    st.subheader("Sustainability Advice:")
    st.write(expert_advice["advice"])
