import sqlite3

DATABASE_NAME = 'farming_data.db'

def create_tables():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Farm Records
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS farm_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            soil_type TEXT NOT NULL,
            location TEXT NOT NULL,
            previous_crop TEXT,
            water_availability TEXT,
            preference TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Weather Forecasts
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather_forecasts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT NOT NULL,
            forecast_date DATE NOT NULL,
            temperature REAL,
            rainfall REAL,
            humidity REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Market Recommendations
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS market_recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            crop TEXT NOT NULL,
            expected_profit REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Sustainability Scores
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sustainability_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            soil_type TEXT NOT NULL,
            location TEXT NOT NULL,
            previous_crop TEXT,
            water_availability TEXT,
            score REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print(f"Database '{DATABASE_NAME}' and tables created successfully.")

if __name__ == '__main__':
    create_tables()