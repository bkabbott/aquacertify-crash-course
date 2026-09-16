# Copy this file, change the question and the values, run it.
import mysql.connector

sql = """
    SELECT wells.name, routes.name AS route
    FROM wells
    JOIN routes ON routes.id = wells.route_id
    WHERE wells.organization_id = %s
    ORDER BY wells.name
"""
values = (1,)

conn = mysql.connector.connect(
    host="127.0.0.1", user="aquacertify", password="aquacertify",
    database="aquacertify", charset="utf8mb4", collation="utf8mb4_general_ci",
)
cursor = conn.cursor(dictionary=True)
cursor.execute(sql, values)
rows = cursor.fetchall()
conn.close()

for row in rows:
    print(row)

print(f"\n{len(rows)} rows")
