# JOIN: show each well with the NAME of its route and system, not the id numbers.
import mysql.connector

conn = mysql.connector.connect(
    host="127.0.0.1", user="aquacertify", password="aquacertify",
    database="aquacertify", charset="utf8mb4", collation="utf8mb4_general_ci",
)
cursor = conn.cursor(dictionary=True)

sql = """
    SELECT wells.name AS well, routes.name AS route, systems.name AS system_name
    FROM wells
    JOIN routes  ON routes.id  = wells.route_id
    JOIN systems ON systems.id = wells.system_id
    WHERE wells.organization_id = %s
    ORDER BY routes.name, wells.name
"""
cursor.execute(sql, (1,))

for row in cursor.fetchall():
    print(f"{row['route']:12} {row['well']:22} {row['system_name']}")

conn.close()
