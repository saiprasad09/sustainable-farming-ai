from agents.farmer_agent import FarmerAgent
from agents.market_agent import MarketAgent
from agents.weather_agent import WeatherAgent
from agents.expert_agent import ExpertAgent
from database import create_tables

if __name__ == "__main__":
    # Initialize database tables
    create_tables()

    # Initialize agents
    farmer_agent = FarmerAgent()
    market_agent = MarketAgent()
    weather_agent = WeatherAgent()
    expert_agent = ExpertAgent()

    # Simulate farmer input
    farmer_data = farmer_agent.process_input()
    print("Farmer Input:", farmer_data)
    farmer_agent.store_farm_record(farmer_data)

    # Get weather forecast
    weather_forecast = farmer_agent.collaborate_with_weather_agent(farmer_data['location'], weather_agent)
    print("Weather Forecast:", weather_forecast)

    # Get profitable crop suggestion
    market_suggestion = farmer_agent.collaborate_with_market_agent(market_agent)
    print("Market Suggestion:", market_suggestion)

    # Get sustainability advice
    sustainability_advice = farmer_agent.collaborate_with_expert_agent(farmer_data, expert_agent)
    print("Sustainability Advice:", sustainability_advice)

    # Example of querying data stored in the database
    print("\n--- Database Queries ---")
    farm_records = farmer_agent.query_database("SELECT * FROM farm_records")
    print("Farm Records:", farm_records)

    weather_data = weather_agent.query_database(f"SELECT * FROM weather_forecasts WHERE location = '{farmer_data['location']}'")
    print("Weather Data:", weather_data)

    market_recommendations = market_agent.query_database("SELECT * FROM market_recommendations")
    print("Market Recommendations:", market_recommendations)

    sustainability_scores = expert_agent.query_database(f"SELECT * FROM sustainability_scores WHERE location = '{farmer_data['location']}'")
    print("Sustainability Scores:", sustainability_scores)