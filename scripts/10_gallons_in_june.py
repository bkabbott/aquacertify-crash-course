# Gallons pumped by each well in a month.
# The meter is like an odometer, so gallons = (end reading - start reading).
# Some meters have fixed zeros painted on the dial, so we multiply by 10 ** fixed_zeros.
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
           well_meters.fixed_zeros,
           MAX(meter_reading) - MIN(meter_reading) AS dial_difference
    FROM well_readings
    JOIN wells       ON wells.id = well_readings.well_id
    JOIN well_meters ON well_meters.id = well_readings.meter_id
    WHERE wells.organization_id = %s
      AND date_of_reading BETWEEN %s AND %s
      AND well_meters.active = 1
    GROUP BY wells.name, well_meters.fixed_zeros
    ORDER BY wells.name
"""
cursor.execute(sql, (1, start, end))

total = 0
for row in cursor.fetchall():
    gallons = row["dial_difference"] * 10 ** row["fixed_zeros"]
    total = total + gallons
    print(f"{row['well']:22} {gallons:>15,}")

print()
print(f"Total: {total:,} gallons")

conn.close()
