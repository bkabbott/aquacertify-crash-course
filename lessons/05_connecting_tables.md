# Lesson 5 - Connecting tables with JOIN

Wells know their route only as a number: `route_id = 4`. The name
"Black Creek" lives in the `routes` table, in the row whose `id` is 4.
You could look it up by hand... or ask the database to do it. That is a
**JOIN**, and it is the single most useful thing in SQL.

## Names instead of numbers

`scripts/07_wells_with_route_names.py`
```python
# JOIN: show each well with the NAME of its route and system, not the id numbers.
import mysql.connector

conn = mysql.connector.connect(
    host="127.0.0.1", user="aquacertify", password="aquacertify",
    database="aquacertify", charset="utf8mb4", collation="utf8mb4_general_ci",
)
cursor = conn.cursor(dictionary=True)

sql = """
    SELECT wells.name AS well, routes.name AS route, systems.name AS system_name
    FROM wells
    JOIN routes  ON routes.id  = wells.route_id
    JOIN systems ON systems.id = wells.system_id
    WHERE wells.organization_id = %s
    ORDER BY routes.name, wells.name
"""
cursor.execute(sql, (1,))

for row in cursor.fetchall():
    print(f"{row['route']:12} {row['well']:22} {row['system_name']}")

conn.close()
```

Output:
```
Black Creek  Black Creek 1 & 2      Hayden Lks.
Effingham    Copperfield 1 & 2      Copperfield Est.
Effingham    Cypress Lakes          Cypress Lakes Subdivision
Effingham    EPOC                   Westwood Heights Subdivision
Effingham    Mill Creek Upper Fl.   Mill Creek Subdivision
Effingham    Mulberry Way           Westwood Heights Subdivision
Effingham    Sandy Woods            Sandy Woods Subdivision
Effingham    South Pointe           South Pointe Subdivision
Effingham    Twenty-One-Centre      Twenty-One-Centre
Effingham    Westwood Heights       Westwood Heights Subdivision
Islands      East Pines             East Pines Subdivision
Islands      Golden Isles           Golden Isles
Islands      Whitemarsh             Whitemarsh Estates
Larchmont    Barbour Point          Larchmont Estates Subdivision
...
```

Read the JOIN line as: "line up each well with the routes row whose id
equals the well's route_id". After that, columns from both tables are
available in the SELECT.

Details worth noticing:

- **`wells.name` and `routes.name`** - both tables have a column called
  `name`, so we say which one we mean with `table.column`.
- **`AS well`, `AS route`** - gives the column a clearer label in the answer.
  (We use `system_name` rather than `system` because SYSTEM is a word SQL
  keeps for itself.)
- **Each extra JOIN adds one more table.** This is how you follow the lines
  in the map from lesson 2.
- The `print(f"...")` line uses `{row['route']:12}` to pad the text to 12
  characters so the columns line up. Purely cosmetic.

## A day's work: readings with well and technician

`scripts/08_readings_on_a_day.py`
```python
# Everything that was read on one day, with the well and technician names.
import mysql.connector

day = "2026-07-06"

conn = mysql.connector.connect(
    host="127.0.0.1", user="aquacertify", password="aquacertify",
    database="aquacertify", charset="utf8mb4", collation="utf8mb4_general_ci",
)
cursor = conn.cursor(dictionary=True)

sql = """
    SELECT wells.name AS well,
           well_readings.meter_reading,
           well_readings.chlorine_residual,
           users.first_name AS technician
    FROM well_readings
    JOIN wells ON wells.id = well_readings.well_id
    LEFT JOIN users ON users.id = well_readings.user_id
    WHERE wells.organization_id = %s AND well_readings.date_of_reading = %s
    ORDER BY wells.name
"""
cursor.execute(sql, (1, day))

for row in cursor.fetchall():
    print(f"{row['well']:22} {row['meter_reading']:>12} {row['chlorine_residual']}  {row['technician']}")

conn.close()
```

Output:
```
Barbour Point             760396975 1.2  Joshua
Berwick Lakes             420871298 1.2  Justin
Black Creek 1 & 2            987752 0.8  Eric
Copperfield 1 & 2          46351000 0.8  Eric
Cottonvale                 50599597 1.5  Dylan
Cypress Lakes               8417800 0.8  Eric
East Pines                334260000 1.0  Kim
Elevated Tank (Well)       70280630 1.5  Eddie
Enclave                   388828187 1.5  EJ
EPOC                      363241000 0.8  Eric
Golden Isles               37791380 1.2  Kim
Lakes at Cottonvale       254111619 1.5  Dylan
Larchmont                 506711528 1.2  Albert 
Little Neck                19129200 1.5  Joshua
...
```

This is "everything that was read on July 6th" - what an operator looks at
when checking a technician's day.

**LEFT JOIN vs JOIN.** Some older readings were imported and have no
technician (`user_id` is empty). A plain `JOIN users` would silently drop
those rows. `LEFT JOIN` keeps them and shows the technician as `None`.
Rule of thumb: when the linked thing might be missing, use LEFT JOIN.

## The in-between table

A technician can have many routes, and a route many technicians. That
cannot be stored as one `route_id` column on the user. Instead there is a
small table `users_routes` that just holds pairs of (user_id, route_id).
Joining *through* it connects the two:

```sql
SELECT users.first_name, routes.name AS route
FROM users
JOIN users_routes ON users_routes.user_id = users.id
JOIN routes       ON routes.id = users_routes.route_id
WHERE users.organization_id = 1 AND users.technician = 1
ORDER BY users.first_name, routes.name
```

You will see the same trick with `meters_sli_ga_addresses` (customer meters
to addresses).

## Things to try

1. In `07_wells_with_route_names.py`, add `wells.latitude` to the SELECT and print it.
2. Change `08_readings_on_a_day.py` to a different day. Try a Sunday.
3. Put the `users_routes` query above into a copy of `07` and run it.
4. Use lesson 1's `SHOW CREATE TABLE lift_stations\G` to find what
   `lift_stations` links to, then write a query listing lift stations with
   their route names.

Next: [Lesson 6 - Counting and totals](06_counting_and_totals.md)
