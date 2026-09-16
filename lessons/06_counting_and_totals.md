# Lesson 6 - Counting and totals

"How many?" "What is the average?" "How much did we pump?" These are the
questions that matter to an operator, and they need one more idea:
**GROUP BY** - one summary row per well (or per route, or per person).

## One row per well

`scripts/09_readings_per_well.py`
```python
# One summary row per well for a month: how many readings, average / lowest / highest chlorine.
import mysql.connector

start = "2026-06-01"
end = "2026-06-30"

conn = mysql.connector.connect(
    host="127.0.0.1", user="aquacertify", password="aquacertify",
    database="aquacertify", charset="utf8mb4", collation="utf8mb4_general_ci",
)
cursor = conn.cursor(dictionary=True)

sql = """
    SELECT wells.name AS well,
           COUNT(*) AS readings,
           ROUND(AVG(chlorine_residual), 2) AS avg_chlorine,
           MIN(chlorine_residual) AS lowest,
           MAX(chlorine_residual) AS highest
    FROM well_readings
    JOIN wells ON wells.id = well_readings.well_id
    WHERE wells.organization_id = %s AND date_of_reading BETWEEN %s AND %s
    GROUP BY wells.name
    ORDER BY avg_chlorine
"""
cursor.execute(sql, (1, start, end))

print(f"{'well':22} {'readings':>8} {'avg':>5} {'low':>5} {'high':>5}")
for row in cursor.fetchall():
    print(f"{row['well']:22} {row['readings']:>8} {row['avg_chlorine']:>5} {row['lowest']:>5} {row['highest']:>5}")

conn.close()
```

Output:
```
well                   readings   avg   low  high
Westwood Heights             30  0.80   0.8   0.8
Copperfield 1 & 2            30  0.80   0.8   0.8
Twenty-One-Centre            30  0.80   0.8   0.8
Black Creek 1 & 2            30  0.80   0.8   0.8
South Pointe                 30  0.80   0.8   0.8
Sandy Woods                  30  0.80   0.8   0.8
Cypress Lakes                30  0.80   0.8   0.8
EPOC                         30  0.80   0.8   0.8
Regency                      30  0.80   0.8   0.8
Mill Creek Upper Fl.         30  0.81   0.8   1.0
Mulberry Way                 30  0.99   0.8   1.0
East Pines                   30  1.05   0.8   1.2
Parish Way                   28  1.12   1.0   1.5
...
```

`GROUP BY wells.name` means "give me one row per well". Then `COUNT`,
`AVG`, `MIN` and `MAX` each summarise that well's readings into one
number. `ROUND(..., 2)` trims the average to two decimals.

Look at the lowest chlorine numbers. A well that is consistently low is
exactly what an operator wants to spot quickly - and you just built that
report.

`BETWEEN 'start' AND 'end'` is the easy way to say "in June".

## Gallons pumped

The meter dial is like an odometer, so gallons pumped in a month is
simply (reading at the end) minus (reading at the start): `MAX - MIN`.

One catch: some meters have fixed zeros painted on the end of the dial -
the dial shows 123456 but means 12,345,600. The `well_meters` table has a
column `fixed_zeros` that says how many.

`scripts/10_gallons_in_june.py`
```python
# Gallons pumped by each well in a month.
# The meter is like an odometer, so gallons = (end reading - start reading).
# Some meters have fixed zeros painted on the dial, so we multiply by 10 ** fixed_zeros.
import mysql.connector

start = "2026-06-01"
end = "2026-06-30"

conn = mysql.connector.connect(
    host="127.0.0.1", user="aquacertify", password="aquacertify",
    database="aquacertify", charset="utf8mb4", collation="utf8mb4_general_ci",
)
cursor = conn.cursor(dictionary=True)

sql = """
    SELECT wells.name AS well,
           well_meters.fixed_zeros,
           MAX(meter_reading) - MIN(meter_reading) AS dial_difference
    FROM well_readings
    JOIN wells       ON wells.id = well_readings.well_id
    JOIN well_meters ON well_meters.id = well_readings.meter_id
    WHERE wells.organization_id = %s
      AND date_of_reading BETWEEN %s AND %s
      AND well_meters.active = 1
    GROUP BY wells.name, well_meters.fixed_zeros
    ORDER BY wells.name
"""
cursor.execute(sql, (1, start, end))

total = 0
for row in cursor.fetchall():
    gallons = row["dial_difference"] * 10 ** row["fixed_zeros"]
    total = total + gallons
    print(f"{row['well']:22} {gallons:>15,}")

print()
print(f"Total: {total:,} gallons")

conn.close()
```

Output:
```
Barbour Point               11,844,650
Berwick Lakes               11,316,307
Black Creek 1 & 2               80,013
Copperfield 1 & 2          541,000,000
Cottonvale                     593,742
Cypress Lakes               12,300,000
East Pines               1,040,000,000
Elevated Tank (Well)         1,500,952
Enclave                      5,975,965
EPOC                     2,053,000,000
Golden Isles                 1,190,440
Lakes at Cottonvale          3,673,586
Larchmont                    1,309,404
Little Neck                 20,020,000
...
```

Here the database does the grouping and Python does the last bit of
arithmetic. Look at the loop:

```python
gallons = row["dial_difference"] * 10 ** row["fixed_zeros"]   # 10**3 is 1000
total = total + gallons                                        # running sum
```

`total` starts at 0 before the loop and grows by one well each time
round. After the loop it holds the company total. This "start at zero,
add in the loop" pattern is how you total anything in Python.

`{gallons:>15,}` in the print means: right-align in 15 characters, with
thousands separators.

## Who did the most?

`scripts/11_technician_leaderboard.py`
```python
# Who has taken the most readings this year?
import mysql.connector

since = "2026-01-01"

conn = mysql.connector.connect(
    host="127.0.0.1", user="aquacertify", password="aquacertify",
    database="aquacertify", charset="utf8mb4", collation="utf8mb4_general_ci",
)
cursor = conn.cursor(dictionary=True)

sql = """
    SELECT users.first_name, COUNT(*) AS readings
    FROM well_readings
    JOIN wells ON wells.id = well_readings.well_id
    JOIN users ON users.id = well_readings.user_id
    WHERE wells.organization_id = %s AND date_of_reading >= %s
    GROUP BY users.first_name
    ORDER BY readings DESC
"""
cursor.execute(sql, (1, since))

for row in cursor.fetchall():
    print(f"{row['first_name']:12} {row['readings']:>6}")

conn.close()
```

Output:
```
Eric           1551
Justin          646
Kim             562
Eddie           467
John            332
EJ              294
Dylan           256
William         228
Joshua          209
Albert          108
Thomas           12
Logan             9
```

Same shape: JOIN to get the name, GROUP BY the name, COUNT, ORDER BY the
count. Once you have seen this pattern three times you can write it for
anything.

## Things to try

1. In `09_readings_per_well.py`, change the month to May.
2. In `10_gallons_in_june.py`, add `systems.name` (JOIN systems ON
   systems.id = wells.system_id, and add it to GROUP BY) so you can see
   gallons per subdivision.
3. Change `11_technician_leaderboard.py` to count `station_readings`
   instead (`JOIN lift_stations ON lift_stations.id = station_readings.lift_station_id`).
4. Average rainfall per month: `SELECT DATE_FORMAT(date_of_reading, '%Y-%m') AS month, ROUND(AVG(rainfall), 2) FROM station_readings GROUP BY month`.

Next: [Lesson 7 - Rain and pumps](07_rain_and_pumps.md)
