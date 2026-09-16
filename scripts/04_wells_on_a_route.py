# Only the wells on one route. Change route_number and run again.
import mysql.connector

route_number = 4          # 1 = Larchmont, 2 = Effingham, 3 = Islands, 4 = Black Creek

conn = mysql.connector.connect(
    host="127.0.0.1", user="aquacertify", password="aquacertify",
    database="aquacertify", charset="utf8mb4", collation="utf8mb4_general_ci",
)
cursor = conn.cursor(dictionary=True)

sql = "SELECT name, source_number FROM wells WHERE route_id = %s"
cursor.execute(sql, (route_number,))       # %s is a blank; the value goes in a tuple

for row in cursor.fetchall():
    print(row["name"], "-", row["source_number"])

conn.close()
