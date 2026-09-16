# Who has taken the most readings this year?
import mysql.connector

since = "2026-01-01"

conn = mysql.connector.connect(
    host="127.0.0.1", user="aquacertify", password="aquacertify",
    database="aquacertify", charset="utf8mb4", collation="utf8mb4_general_ci",
)
cursor = conn.cursor(dictionary=True)

sql = """
    SELECT users.first_name, COUNT(*) AS readings
    FROM well_readings
    JOIN wells ON wells.id = well_readings.well_id
    JOIN users ON users.id = well_readings.user_id
    WHERE wells.organization_id = %s AND date_of_reading >= %s
    GROUP BY users.first_name
    ORDER BY readings DESC
"""
cursor.execute(sql, (1, since))

for row in cursor.fetchall():
    print(f"{row['first_name']:12} {row['readings']:>6}")

conn.close()
