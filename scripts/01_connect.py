# Connect to the database and prove it worked.
import mysql.connector

conn = mysql.connector.connect(
    host="127.0.0.1",
    user="aquacertify",
    password="aquacertify",
    database="aquacertify",
    charset="utf8mb4",
    collation="utf8mb4_general_ci",
)

cursor = conn.cursor()
cursor.execute("SELECT VERSION()")
print("Connected! Database version:", cursor.fetchone()[0])

conn.close()
