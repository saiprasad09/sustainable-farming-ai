🌱 Sustainable Farming AI Advisor using Multi-Agent System

🌍 Overview  
This is an intelligent, interactive farming advisory system built with Streamlit and AI-driven agents. It empowers farmers to make informed decisions about crop selection, sustainability, and profitability based on real-time environmental and market data. Designed as part of a Gen AI Hackathon challenge.

---

✨ Features  
✅ Easy-to-use web interface powered by Streamlit  
✅ Recommends optimal crops based on soil, weather, and climate  
✅ Predicts sustainability scores from farming practices  
✅ Estimates profit using market trends and price forecasting  
✅ Integrates multiple agents (Farmer, Weather, Expert, Market)  
✅ Uses real farmer and market datasets  
✅ Fully deployable on Streamlit Cloud

---

🛠️ Technologies Used  
🐍 Python (core logic)  
🌐 Streamlit (web app interface)  
📊 Pandas, NumPy (data handling)  
🤖 Scikit-learn (ML for prediction)  
🗂️ SQLite (long-term memory storage)  
🧠 Modular agent-based architecture  

---

📂 Dataset & Model  
This project uses real datasets with the following parameters:

🧪 Soil pH, Moisture, Temperature, Rainfall  
🌾 Crop Type, Fertilizer & Pesticide Use  
📈 Market Price, Competitor Price, Demand Index  
🌦️ Weather Impact Score, Seasonal Factors

ML models used:
- RandomForest or DecisionTree (Crop Recommender)
- Custom logic (Sustainability Estimator)

---

💻 Installation & Running Locally

1️⃣ Clone the Repository  
```bash

git clone https://github.com/Saiprasad09/sustainable-farming-ai.git
cd sustainable-farming-ai
gipip install -r requirements.txt
streamlit run app.py

