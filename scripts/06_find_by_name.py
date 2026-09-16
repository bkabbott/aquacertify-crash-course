# Find wells whose name contains some text.
import mysql.connector

search = "Lake"

conn = mysql.connector.connect(
    host="127.0.0.1", user="aquacertify", password="aquacertify",
    database="aquacertify", charset="utf8mb4", collation="utf8mb4_general_ci",
)
cursor = conn.cursor(dictionary=True)

sql = """
    SELECT name, latitude, longitude
    FROM wells
    WHERE organization_id = %s AND name LIKE %s
    ORDER BY name
"""
cursor.execute(sql, (1, "%" + search + "%"))   # % means "anything" in LIKE

for row in cursor.fetchall():
    print(row["name"])

conn.close()
