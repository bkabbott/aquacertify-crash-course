# Everything that was read on one day, with the well and technician names.
import mysql.connector

day = "2026-07-06"

conn = mysql.connector.connect(
    host="127.0.0.1", user="aquacertify", password="aquacertify",
    database="aquacertify", charset="utf8mb4", collation="utf8mb4_general_ci",
)
cursor = conn.cursor(dictionary=True)

sql = """
    SELECT wells.name AS well,
           well_readings.meter_reading,
           well_readings.chlorine_residual,
           users.first_name AS technician
    FROM well_readings
    JOIN wells ON wells.id = well_readings.well_id
    LEFT JOIN users ON users.id = well_readings.user_id
    WHERE wells.organization_id = %s AND well_readings.date_of_reading = %s
    ORDER BY wells.name
"""
cursor.execute(sql, (1, day))

for row in cursor.fetchall():
    print(f"{row['well']:22} {row['meter_reading']:>12} {row['chlorine_residual']}  {row['technician']}")

conn.close()
