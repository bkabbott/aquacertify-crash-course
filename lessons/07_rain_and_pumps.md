# Lesson 7 - Rain and pumps: a discovery hiding in the data

A lift station is a pit where sewage collects, with two pumps that push it
up and onward. Each pump has an hour-meter - a dial counting how many
hours the pump has run. Every day a technician writes down both dials and
how much rain fell. That is `station_readings`: `pump1`, `pump2`,
`rainfall`, `date_of_reading`.

Here is a question an operator genuinely cares about: **when it rains,
does rainwater leak into the sewer pipes and make the pumps run longer?**
(In the trade: "inflow and infiltration".) Let's find out.

## The whole picture in one question

`scripts/12_rain_and_pumps.py`
```python
# Does rain make the sewer pumps run longer?
# For every station and day: pump hours = today's dial - yesterday's dial.
# Then group the days by how much it rained and average the hours.
import mysql.connector

since = "2025-01-01"

conn = mysql.connector.connect(
    host="127.0.0.1", user="aquacertify", password="aquacertify",
    database="aquacertify", charset="utf8mb4", collation="utf8mb4_general_ci",
)
cursor = conn.cursor(dictionary=True)

sql = """
    WITH daily AS (
        SELECT rainfall,
               (pump1 - LAG(pump1) OVER (PARTITION BY lift_station_id ORDER BY date_of_reading))
             + (pump2 - LAG(pump2) OVER (PARTITION BY lift_station_id ORDER BY date_of_reading)) AS hours
        FROM station_readings
        WHERE date_of_reading >= %s
    )
    SELECT CASE WHEN rainfall = 0   THEN '1. dry'
                WHEN rainfall < 0.5 THEN '2. light rain'
                ELSE                     '3. heavy rain' END AS weather,
           COUNT(*) AS station_days,
           ROUND(AVG(hours), 2) AS average_pump_hours
    FROM daily
    WHERE hours BETWEEN 0 AND 48
    GROUP BY weather
    ORDER BY weather
"""
cursor.execute(sql, (since,))

for row in cursor.fetchall():
    print(f"{row['weather']:16} {row['station_days']:>7} days   {row['average_pump_hours']} hours/day")

conn.close()
```

Output:
```
1. dry             23152 days   4.02 hours/day
2. light rain       2303 days   4.60 hours/day
3. heavy rain       1426 days   5.15 hours/day
```

There it is. On dry days the pumps run about 4 hours; on heavy-rain days,
over 5. Rain **is** getting into the sewers. That used to take an
afternoon with a calculator; the database answered it in a blink, across
27,000 station-days.

You do not need to memorise this SQL. What it does, in English:

1. `WITH daily AS (...)` - first, build a temporary table called `daily`.
2. `LAG(pump1)` - "the previous day's pump1 reading". So
   `pump1 - LAG(pump1)` is hours run today. `PARTITION BY lift_station_id`
   keeps each station's days separate.
3. `CASE WHEN ... THEN ... END` - sort each day into a bucket by rainfall.
4. `GROUP BY weather` - one row per bucket, with the average hours.
5. `WHERE hours BETWEEN 0 AND 48` - throw out impossible values (a dial
   that was replaced, or a typo). Always be a little suspicious of raw data.

The lesson is not the syntax. It is: **if you can say the question in
English, the data can usually answer it.**

## The same idea, simpler: hardest-working stations

`scripts/13_hardest_working_stations.py`
```python
# Which lift stations ran their pumps the most in a month?
import mysql.connector

start = "2026-06-01"
end = "2026-06-30"

conn = mysql.connector.connect(
    host="127.0.0.1", user="aquacertify", password="aquacertify",
    database="aquacertify", charset="utf8mb4", collation="utf8mb4_general_ci",
)
cursor = conn.cursor(dictionary=True)

sql = """
    SELECT lift_stations.name,
           ROUND(MAX(pump1) - MIN(pump1), 1) AS pump1_hours,
           ROUND(MAX(pump2) - MIN(pump2), 1) AS pump2_hours,
           ROUND(SUM(rainfall), 2) AS rain_inches
    FROM station_readings
    JOIN lift_stations ON lift_stations.id = station_readings.lift_station_id
    WHERE lift_stations.organization_id = %s AND date_of_reading BETWEEN %s AND %s
    GROUP BY lift_stations.name
    ORDER BY (MAX(pump1) - MIN(pump1)) + (MAX(pump2) - MIN(pump2)) DESC
"""
cursor.execute(sql, (1, start, end))

print(f"{'station':20} {'pump 1':>8} {'pump 2':>8} {'rain':>6}")
for row in cursor.fetchall():
    print(f"{row['name']:20} {row['pump1_hours']:>8} {row['pump2_hours']:>8} {row['rain_inches']:>6}")

conn.close()
```

Output:
```
station                pump 1   pump 2   rain
Southbridge #2        10018.2      2.3   9.35
Salt Creek #1          5046.1     64.8   4.47
Larchmont               126.2    137.7   4.91
Southbridge #1          115.6    113.5  10.48
Circle K                  3.3    215.3   4.54
Enclave #3                0.1    206.0   2.77
Enclave #1               46.1    138.0  10.21
Regency                 176.6      1.3   0.00
Laurel Green             68.4    100.0   3.98
Berwick Boul. #1         96.1     62.3   3.14
Berwick Boul. #2         67.2     89.4   4.75
Willow Lakes             84.2     59.0   6.77
Grand Oaks               72.8     69.8   6.00
...
```

`MAX(pump1) - MIN(pump1)` is the same odometer trick as gallons: end minus
start. If one pump runs far more than its partner, something may be wrong
with the other one. A ten-line question can flag a pump that needs a look
before it fails.

## Things to try

1. In `12_rain_and_pumps.py`, change `since` to `"2026-01-01"`. Does the
   pattern hold this year?
2. Change the `0.5` inch threshold to `1.0`.
3. In `13_hardest_working_stations.py`, sort by `rain_inches DESC` instead.
   Do the rainiest stations also run the most?

Next: [Lesson 8 - The lead pipe inventory](08_the_lead_pipe_inventory.md)
