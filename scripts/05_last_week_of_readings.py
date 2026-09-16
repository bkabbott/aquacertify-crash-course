# The most recent readings for one well, newest first.
import mysql.connector

well_number = 39
how_many = 7

conn = mysql.connector.connect(
    host="127.0.0.1", user="aquacertify", password="aquacertify",
    database="aquacertify", charset="utf8mb4", collation="utf8mb4_general_ci",
)
cursor = conn.cursor(dictionary=True)

sql = """
    SELECT date_of_reading, meter_reading, chlorine_residual
    FROM well_readings
    WHERE well_id = %s
    ORDER BY date_of_reading DESC
    LIMIT %s
"""
cursor.execute(sql, (well_number, how_many))

for row in cursor.fetchall():
    print(row["date_of_reading"], row["meter_reading"], row["chlorine_residual"])

conn.close()
