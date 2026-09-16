# Lesson 4 - Asking better questions

So far: `SELECT columns FROM table`. Three more words cover most of what
an operator ever asks: **WHERE** (only some rows), **ORDER BY** (sorted),
**LIMIT** (just a few). And one trick - the fill-in-the-blank `%s`.

## WHERE: only the rows that match

`scripts/04_wells_on_a_route.py`
```python
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
```

Output:
```
Black Creek 1 & 2 - 101 & 102
```

`WHERE route_id = %s` keeps only wells whose route_id matches.

**The `%s` blank.** Instead of writing the number into the SQL text, we
put `%s` where it goes and hand the value over separately, in round
brackets: `cursor.execute(sql, (route_number,))`. The database fills in
the blank.

Do it this way every time a value comes from a variable. It handles quotes
and dates correctly, and it is the way professionals prevent a nasty class
of security bug. (The odd-looking `(route_number,)` with a trailing comma
is how Python writes a list of one value - a *tuple*.)

## ORDER BY and LIMIT: the newest few

`scripts/05_last_week_of_readings.py`
```python
# The most recent readings for one well, newest first.
import mysql.connector

well_number = 39
how_many = 7

conn = mysql.connector.connect(
    host="127.0.0.1", user="aquacertify", password="aquacertify",
    database="aquacertify", charset="utf8mb4", collation="utf8mb4_general_ci",
)
cursor = conn.cursor(dictionary=True)

sql = """
    SELECT date_of_reading, meter_reading, chlorine_residual
    FROM well_readings
    WHERE well_id = %s
    ORDER BY date_of_reading DESC
    LIMIT %s
"""
cursor.execute(sql, (well_number, how_many))

for row in cursor.fetchall():
    print(row["date_of_reading"], row["meter_reading"], row["chlorine_residual"])

conn.close()
```

Output:
```
2026-07-07 363294000 0.8
2026-07-06 363241000 0.8
2026-07-05 363202000 0.8
2026-07-04 363160000 0.8
2026-07-03 363131000 0.8
2026-07-02 363025000 0.8
2026-07-01 362928000 0.8
```

`ORDER BY date_of_reading DESC` = newest first (DESC = descending). Leave
off DESC for oldest first. So this reads: "the last 7 days of readings for
well 39" - a question an operator asks all the time.

Two blanks this time, so two values in the tuple, in the same order.

The SQL is inside triple quotes `"""` so it can span several lines. Lay it
out however reads best; the database does not care about line breaks.

## LIKE: searching text

`scripts/06_find_by_name.py`
```python
# Find wells whose name contains some text.
import mysql.connector

search = "Lake"

conn = mysql.connector.connect(
    host="127.0.0.1", user="aquacertify", password="aquacertify",
    database="aquacertify", charset="utf8mb4", collation="utf8mb4_general_ci",
)
cursor = conn.cursor(dictionary=True)

sql = """
    SELECT name, latitude, longitude
    FROM wells
    WHERE organization_id = %s AND name LIKE %s
    ORDER BY name
"""
cursor.execute(sql, (1, "%" + search + "%"))   # % means "anything" in LIKE

for row in cursor.fetchall():
    print(row["name"])

conn.close()
```

Output:
```
Berwick Lakes
Cypress Lakes
Lakes at Cottonvale
Willow Lakes Drive
```

`LIKE` matches text with `%` as a wildcard meaning "anything here".
`"%Lake%"` = anything containing Lake. (Yes, that `%` is a different thing
from the `%s` blank - it is inside the value, not the SQL.)

`AND` joins two conditions. `organization_id = 1` narrows to the real
company rather than the practice copy - you will see it in every script
from now on.

## Dates

Dates are written as text in the form `'YYYY-MM-DD'`. Useful comparisons:

```sql
WHERE date_of_reading = '2026-07-06'
WHERE date_of_reading >= '2026-07-01'
WHERE date_of_reading BETWEEN '2026-06-01' AND '2026-06-30'
```

## Things to try

1. In `04_wells_on_a_route.py`, change `route_number` to 1, 2 and 3.
2. In `05_last_week_of_readings.py`, change `how_many` to 30 and look at the
   meter reading going up day by day.
3. Change `06_find_by_name.py` to search for `"Creek"`.
4. Write a script that shows the 5 lowest chlorine readings ever for well 39:
   `ORDER BY chlorine_residual` (no DESC) and `LIMIT 5`.

Next: [Lesson 5 - Connecting tables](05_connecting_tables.md)
