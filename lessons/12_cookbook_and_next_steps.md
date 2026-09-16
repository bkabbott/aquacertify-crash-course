# Lesson 12 - Cookbook and next steps

## Writing your own script

`scripts/21_your_own_query.py` is the template: copy it, change `sql` and
`values`, run it.

```python
# Copy this file, change the question and the values, run it.
import mysql.connector

sql = """
    SELECT wells.name, routes.name AS route
    FROM wells
    JOIN routes ON routes.id = wells.route_id
    WHERE wells.organization_id = %s
    ORDER BY wells.name
"""
values = (1,)

conn = mysql.connector.connect(
    host="127.0.0.1", user="aquacertify", password="aquacertify",
    database="aquacertify", charset="utf8mb4", collation="utf8mb4_general_ci",
)
cursor = conn.cursor(dictionary=True)
cursor.execute(sql, values)
rows = cursor.fetchall()
conn.close()

for row in rows:
    print(row)

print(f"\n{len(rows)} rows")
```

```bash
cp scripts/21_your_own_query.py low_chlorine.py
# edit low_chlorine.py
python3 low_chlorine.py
```

When you want the answer in a spreadsheet, add the `Workbook` lines from
lesson 9 at the bottom instead of the `print` loop.

## Recipes

Questions an operator might actually ask. Each one uses only lessons 4-6:
SELECT, JOIN, WHERE, GROUP BY, ORDER BY, and `%s` blanks. Paste the SQL
into the template above (or into the command line from lesson 1 with the
blanks filled in and a `;` on the end).

**What did well 39 read in the last two days?**
```sql
SELECT date_of_reading, meter_reading, chlorine_residual, comment
FROM well_readings
WHERE well_id = %s
ORDER BY date_of_reading DESC LIMIT 2
```
values: `(39,)`

**When was each well last read? (oldest first - a missed-stop check)**
```sql
SELECT wells.name, MAX(well_readings.date_of_reading) AS last_read
FROM wells
LEFT JOIN well_readings ON well_readings.well_id = wells.id
WHERE wells.organization_id = %s
GROUP BY wells.name
ORDER BY last_read
```
values: `(1,)`

**Any chlorine readings below 0.5 since June?**
```sql
SELECT well_readings.date_of_reading, wells.name, well_readings.chlorine_residual
FROM well_readings
JOIN wells ON wells.id = well_readings.well_id
WHERE wells.organization_id = %s AND well_readings.date_of_reading >= %s
  AND well_readings.chlorine_residual < %s
ORDER BY well_readings.chlorine_residual
```
values: `(1, "2026-06-01", 0.5)`

**What comments have technicians left lately?**
```sql
SELECT well_readings.date_of_reading, wells.name, users.first_name, well_readings.comment
FROM well_readings
JOIN wells ON wells.id = well_readings.well_id
LEFT JOIN users ON users.id = well_readings.user_id
WHERE wells.organization_id = %s AND well_readings.comment IS NOT NULL
  AND well_readings.date_of_reading >= %s
ORDER BY well_readings.date_of_reading DESC
```
values: `(1, "2026-04-01")`

**How much rain fell at each lift station in June?**
```sql
SELECT lift_stations.name, ROUND(SUM(rainfall), 2) AS inches
FROM station_readings
JOIN lift_stations ON lift_stations.id = station_readings.lift_station_id
WHERE lift_stations.organization_id = %s AND date_of_reading BETWEEN %s AND %s
GROUP BY lift_stations.name
ORDER BY inches DESC
```
values: `(1, "2026-06-01", "2026-06-30")`

**Which wells are on which permit, from which aquifer?**
```sql
SELECT wells.name AS well, permits.permit_number, aquifers.name AS aquifer
FROM wells
JOIN groundwater_withdrawal_permits AS permits ON permits.id = wells.groundwater_withdrawal_permit_id
JOIN aquifers ON aquifers.id = permits.aquifer_id
WHERE wells.organization_id = %s
ORDER BY permits.permit_number
```
values: `(1,)`

**Where is a well? (GPS to paste into Google Maps)**
```sql
SELECT name, CONCAT(latitude, ', ', longitude) AS paste_into_maps
FROM wells
WHERE organization_id = %s AND name LIKE %s
```
values: `(1, "%Cypress%")`

**Which technician reads which routes?**
```sql
SELECT users.first_name, routes.name AS route
FROM users
JOIN users_routes ON users_routes.user_id = users.id
JOIN routes       ON routes.id = users_routes.route_id
WHERE users.organization_id = %s AND users.technician = 1
ORDER BY users.first_name, routes.name
```
values: `(1,)`

**Errors from the app, most common first**
```sql
SELECT LEFT(error, 80) AS what_went_wrong, COUNT(*) AS times
FROM errors
GROUP BY what_went_wrong
ORDER BY times DESC
LIMIT 10
```
values: `()`

## When something goes wrong

Read the **last line** of the error first, then find the line number it
mentions.

| You see | It means |
|---|---|
| `ModuleNotFoundError: No module named 'mysql'` | you forgot `source .venv/bin/activate` |
| `SyntaxError` | a typo in the Python: missing quote, bracket, colon, or wrong indentation |
| `ProgrammingError ... syntax` | a typo in the SQL, or a column named with an SQL word (lines, system, order...) |
| `Unknown column 'x'` | check the spelling against DATABASE_INDEX.md or `DESCRIBE table;` |
| `KeyError: 'nmae'` | you asked a row for a column that is not in the SELECT (spelling) |
| `Not all parameters were used` / `Not enough parameters` | the number of `%s` blanks and values do not match |
| an empty answer | print the values you passed; a typo in a date or name is the usual cause |
| `FileNotFoundError: output/...` | run the script from the course folder, not from inside `scripts/` |

## Where to go from here

- `DATABASE_INDEX.md` - the full map. Browse the tables you have not used yet.
- `PYTHON_BASICS.md` - one page of Python for when a line looks strange.
- The `mariadb` command line (lesson 1) is the quickest way to try an idea
  before putting it in a script.
- Every script here only reads. When you are ready to learn how data gets
  *into* the database (INSERT, UPDATE), practise on organization 2 - the
  copy - never on organization 1.
