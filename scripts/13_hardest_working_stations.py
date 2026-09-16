# Which lift stations ran their pumps the most in a month?
import mysql.connector

start = "2026-06-01"
end = "2026-06-30"

conn = mysql.connector.connect(
    host="127.0.0.1", user="aquacertify", password="aquacertify",
    database="aquacertify", charset="utf8mb4", collation="utf8mb4_general_ci",
)
cursor = conn.cursor(dictionary=True)

sql = """
    SELECT lift_stations.name,
           ROUND(MAX(pump1) - MIN(pump1), 1) AS pump1_hours,
           ROUND(MAX(pump2) - MIN(pump2), 1) AS pump2_hours,
           ROUND(SUM(rainfall), 2) AS rain_inches
    FROM station_readings
    JOIN lift_stations ON lift_stations.id = station_readings.lift_station_id
    WHERE lift_stations.organization_id = %s AND date_of_reading BETWEEN %s AND %s
    GROUP BY lift_stations.name
    ORDER BY (MAX(pump1) - MIN(pump1)) + (MAX(pump2) - MIN(pump2)) DESC
"""
cursor.execute(sql, (1, start, end))

print(f"{'station':20} {'pump 1':>8} {'pump 2':>8} {'rain':>6}")
for row in cursor.fetchall():
    print(f"{row['name']:20} {row['pump1_hours']:>8} {row['pump2_hours']:>8} {row['rain_inches']:>6}")

conn.close()
