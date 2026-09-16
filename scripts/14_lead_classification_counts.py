# The lead pipe inventory: how many service lines of each kind?
import mysql.connector

conn = mysql.connector.connect(
    host="127.0.0.1", user="aquacertify", password="aquacertify",
    database="aquacertify", charset="utf8mb4", collation="utf8mb4_general_ci",
)
cursor = conn.cursor(dictionary=True)

sql = """
    SELECT answers.response AS classification, COUNT(*) AS how_many
    FROM sli_ga_service_lines
    JOIN sli_ga_overall_service_line_classification_responses AS answers
      ON answers.id = sli_ga_service_lines.overall_service_line_classification_id
    WHERE sli_ga_service_lines.organization_id = %s
    GROUP BY answers.response
    ORDER BY how_many DESC
"""
cursor.execute(sql, (1,))

for row in cursor.fetchall():
    print(f"{row['classification']:25} {row['how_many']:>6}")

conn.close()
