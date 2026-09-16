# Does rain make the sewer pumps run longer?
# For every station and day: pump hours = today's dial - yesterday's dial.
# Then group the days by how much it rained and average the hours.
import mysql.connector

since = "2025-01-01"

conn = mysql.connector.connect(
    host="127.0.0.1", user="aquacertify", password="aquacertify",
    database="aquacertify", charset="utf8mb4", collation="utf8mb4_general_ci",
)
cursor = conn.cursor(dictionary=True)

sql = """
    WITH daily AS (
        SELECT rainfall,
               (pump1 - LAG(pump1) OVER (PARTITION BY lift_station_id ORDER BY date_of_reading))
             + (pump2 - LAG(pump2) OVER (PARTITION BY lift_station_id ORDER BY date_of_reading)) AS hours
        FROM station_readings
        WHERE date_of_reading >= %s
    )
    SELECT CASE WHEN rainfall = 0   THEN '1. dry'
                WHEN rainfall < 0.5 THEN '2. light rain'
                ELSE                     '3. heavy rain' END AS weather,
           COUNT(*) AS station_days,
           ROUND(AVG(hours), 2) AS average_pump_hours
    FROM daily
    WHERE hours BETWEEN 0 AND 48
    GROUP BY weather
    ORDER BY weather
"""
cursor.execute(sql, (since,))

for row in cursor.fetchall():
    print(f"{row['weather']:16} {row['station_days']:>7} days   {row['average_pump_hours']} hours/day")

conn.close()
