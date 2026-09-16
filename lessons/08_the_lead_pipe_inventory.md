# Lesson 8 - The lead pipe inventory

The state of Georgia requires every water system to find out what each
customer's service line (the pipe from the main to the house) is made of,
because old ones can be lead. Our tables for this start with `sli_ga_`:

- `sli_ga_addresses` - one row per customer address
- `sli_ga_service_lines` - one row per pipe: material, and the verdict

## Multiple-choice answers live in their own tables

The inventory form has multiple-choice questions. Each question has its
own tiny table of allowed answers, and the big table stores just the
answer's id number. Try this in the database command line:

```sql
SELECT id, response FROM sli_ga_overall_service_line_classification_responses;
```

```
+----+--------------------------------------------------------+
| id | response                                               |
+----+--------------------------------------------------------+
|  6 | Non-Lead                                               |
|  7 | (GNRR) Galvanized Not Requiring Replacement - Non-Lead |
|  8 | (GRR) Galvanized Requiring Replacement - Lead          |
|  9 | Lead                                                   |
| 10 | Lead Status Unknown                                    |
+----+--------------------------------------------------------+
```

So `sli_ga_service_lines.overall_service_line_classification_id` holds
6, 9, 10... and to see the words you JOIN to this table - exactly like
route names in lesson 5. **Every table ending in `_responses` works this way.**

## How many lines of each kind?

`scripts/14_lead_classification_counts.py`
```python
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
```

Output:
```
Non-Lead                    6530
Lead Status Unknown         1998
```

`AS answers` gives the long table name a short nickname so the rest of the
question is readable.

"Lead Status Unknown" is the number the state cares about: those are the
addresses still to be checked.

(Why `how_many` and not `lines`? Because LINES is a word SQL reserves for
itself, and using it causes a confusing "syntax error". If you ever get
one of those, a name clashing with an SQL word is the usual suspect.)

## Progress by route

`scripts/15_lead_progress_by_route.py`
```python
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
```

Output:
```
route        addresses  unknown  non-lead
Larchmont         6824     1107      5717
Islands            505      476        29
Effingham         1085      415       670
Black Creek        114        0       114
```

`SUM(answers.response = 'Lead Status Unknown')` is a neat trick: the
comparison is 1 when true and 0 when false, so summing it counts the
matches. This is essentially the progress report a manager wants each month.

## A work list

`scripts/16_addresses_to_check.py`
```python
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
```

Output:
```
1 Bryan Wood Circle Savannah 31410
1 Fort Bartow Drive Savannah 31410
1 Pelican Cove Savannah 31410
1 Penrose Cove Savannah 31410
1 Riverview Road Savannah 31410
10 Bryan Wood Circle Savannah 31410
10 Penrose Cove Savannah 31410
10 Penrose Drive Savannah 31410
100 Quarterman Drive Savannah 31410
101 East Pines Road Savannah 31410
... 476 addresses in total
```

That list is a work order. `rows[:10]` means "the first ten" - we keep the
full list in `rows` but only print a few. In lesson 11 this list goes into
a spreadsheet a technician can take with them.

## Things to try

1. Change `route_name` to `"Effingham"`.
2. What materials are the pipes? Copy `14` and JOIN
   `sli_ga_specific_service_line_material_responses AS materials ON
   materials.id = sli_ga_service_lines.customer_owned_specific_material_id`,
   grouping by `materials.response`.
3. `DESCRIBE sli_ga_service_lines;` in the command line and count how many
   columns end in `_id`. Each one is a multiple-choice question.

Next: [Lesson 9 - Your first spreadsheet](09_your_first_spreadsheet.md)
