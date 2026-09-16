# Peek at the first five wells.
import mysql.connector

conn = mysql.connector.connect(
    host="127.0.0.1", user="aquacertify", password="aquacertify",
    database="aquacertify", charset="utf8mb4", collation="utf8mb4_general_ci",
)
cursor = conn.cursor(dictionary=True)

cursor.execute("SELECT name, latitude, longitude FROM wells LIMIT 5")

for row in cursor.fetchall():
    print(row["name"], row["latitude"], row["longitude"])

conn.close()
