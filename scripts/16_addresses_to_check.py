# The addresses on one route that still need a lead check - a work list.
import mysql.connector

route_name = "Islands"

conn = mysql.connector.connect(
    host="127.0.0.1", user="aquacertify", password="aquacertify",
    database="aquacertify", charset="utf8mb4", collation="utf8mb4_general_ci",
)
cursor = conn.cursor(dictionary=True)

sql = """
    SELECT sli_ga_addresses.street_address_1 AS address, sli_ga_addresses.city, sli_ga_addresses.zip
    FROM sli_ga_addresses
    JOIN routes ON routes.id = sli_ga_addresses.route_id
    JOIN sli_ga_service_lines ON sli_ga_service_lines.sli_ga_address_id = sli_ga_addresses.id
    JOIN sli_ga_overall_service_line_classification_responses AS answers
      ON answers.id = sli_ga_service_lines.overall_service_line_classification_id
    WHERE sli_ga_addresses.organization_id = %s
      AND routes.name = %s
      AND answers.response = 'Lead Status Unknown'
    ORDER BY sli_ga_addresses.street_address_1
"""
cursor.execute(sql, (1, route_name))
rows = cursor.fetchall()

for row in rows[:10]:                       # just the first ten on screen
    print(row["address"], row["city"], row["zip"])
print(f"... {len(rows)} addresses in total")

conn.close()
