# One summary row per well for a month: how many readings, average / lowest / highest chlorine.
import mysql.connector

start = "2026-06-01"
end = "2026-06-30"

conn = mysql.connector.connect(
    host="127.0.0.1", user="aquacertify", password="aquacertify",
    database="aquacertify", charset="utf8mb4", collation="utf8mb4_general_ci",
)
cursor = conn.cursor(dictionary=True)

sql = """
    SELECT wells.name AS well,
           COUNT(*) AS readings,
           ROUND(AVG(chlorine_residual), 2) AS avg_chlorine,
           MIN(chlorine_residual) AS lowest,
           MAX(chlorine_residual) AS highest
    FROM well_readings
    JOIN wells ON wells.id = well_readings.well_id
    WHERE wells.organization_id = %s AND date_of_reading BETWEEN %s AND %s
    GROUP BY wells.name
    ORDER BY avg_chlorine
"""
cursor.execute(sql, (1, start, end))

print(f"{'well':22} {'readings':>8} {'avg':>5} {'low':>5} {'high':>5}")
for row in cursor.fetchall():
    print(f"{row['well']:22} {row['readings']:>8} {row['avg_chlorine']:>5} {row['lowest']:>5} {row['highest']:>5}")

conn.close()
