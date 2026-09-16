# The simplest possible spreadsheet: the list of wells.
import mysql.connector
from openpyxl import Workbook

conn = mysql.connector.connect(
    host="127.0.0.1", user="aquacertify", password="aquacertify",
    database="aquacertify", charset="utf8mb4", collation="utf8mb4_general_ci",
)
cursor = conn.cursor(dictionary=True)
cursor.execute("""
    SELECT wells.name AS well, routes.name AS route, wells.latitude, wells.longitude
    FROM wells
    JOIN routes ON routes.id = wells.route_id
    WHERE wells.organization_id = %s
    ORDER BY routes.name, wells.name
""", (1,))
rows = cursor.fetchall()
conn.close()

workbook = Workbook()                       # a new, empty spreadsheet file
sheet = workbook.active                     # its first tab
sheet.title = "Wells"

sheet.append(["Well", "Route", "Latitude", "Longitude"])       # row 1: the headers
for row in rows:
    sheet.append([row["well"], row["route"], row["latitude"], row["longitude"]])

workbook.save("output/wells.xlsx")
print(f"Saved output/wells.xlsx with {len(rows)} wells")
