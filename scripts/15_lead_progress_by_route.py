# Lead inventory progress, one row per route.
import mysql.connector

conn = mysql.connector.connect(
    host="127.0.0.1", user="aquacertify", password="aquacertify",
    database="aquacertify", charset="utf8mb4", collation="utf8mb4_general_ci",
)
cursor = conn.cursor(dictionary=True)

sql = """
    SELECT routes.name AS route,
           COUNT(*) AS addresses,
           SUM(answers.response = 'Lead Status Unknown') AS still_unknown,
           SUM(answers.response = 'Non-Lead') AS confirmed_non_lead
    FROM sli_ga_addresses
    JOIN routes ON routes.id = sli_ga_addresses.route_id
    JOIN sli_ga_service_lines ON sli_ga_service_lines.sli_ga_address_id = sli_ga_addresses.id
    JOIN sli_ga_overall_service_line_classification_responses AS answers
      ON answers.id = sli_ga_service_lines.overall_service_line_classification_id
    WHERE sli_ga_addresses.organization_id = %s
    GROUP BY routes.name
    ORDER BY still_unknown DESC
"""
cursor.execute(sql, (1,))

print(f"{'route':12} {'addresses':>9} {'unknown':>8} {'non-lead':>9}")
for row in cursor.fetchall():
    print(f"{row['route']:12} {row['addresses']:>9} {row['still_unknown']:>8} {row['confirmed_non_lead']:>9}")

conn.close()
