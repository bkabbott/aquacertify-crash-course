# Your first question: the organizations in the database.
import mysql.connector

conn = mysql.connector.connect(
    host="127.0.0.1", user="aquacertify", password="aquacertify",
    database="aquacertify", charset="utf8mb4", collation="utf8mb4_general_ci",
)
cursor = conn.cursor(dictionary=True)      # dictionary=True: rows come back with column names

cursor.execute("SELECT name, city FROM organizations")
rows = cursor.fetchall()

print(rows)                                 # the raw answer
print()
for row in rows:                            # one row at a time
    print(row["name"], "is in", row["city"])

conn.close()
