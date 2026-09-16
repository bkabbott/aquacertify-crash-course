# Python basics - the one page you need for this course

You will meet only a handful of Python ideas. Here they are, with the way
they show up in the scripts.

## Variables: giving a value a name
```python
well_number = 39
since = "2026-07-01"          # text goes in quotes
```

## Lists: several things in order
```python
routes = ["Larchmont", "Effingham", "Islands"]
routes[0]        # -> "Larchmont"   (counting starts at 0)
routes[:2]       # -> the first two
len(routes)      # -> 3
```

## Tuples: a list that cannot change - used for the `%s` values
```python
(39,)                     # one value - the trailing comma matters
(1, "2026-06-01", 0.5)    # three values, in the order of the blanks
```

## Dictionaries: labelled values (one row of a table)
```python
row = {"name": "Larchmont", "route_id": 1}
row["name"]      # -> "Larchmont"
```
With `cursor(dictionary=True)` the database hands you a **list of
dictionaries**: one dictionary per row.

## for loops: do something with every item
```python
for row in rows:
    print(row["name"])       # the indented part runs once per row
```

## if: only sometimes
```python
if row["chlorine_residual"] < 0.5:
    flag = "CHECK"
else:
    flag = "ok"
```

## Adding up
```python
total = 0
for row in rows:
    total = total + row["gallons"]
```

## f-strings: putting values into text
```python
print(f"{row['name']} pumped {total:,} gallons")   # :, adds thousands separators
print(f"{row['name']:22} {total:>12,}")            # :22 pads to 22 wide; :>12 right-aligns
```

## Arithmetic
```python
10 ** 3          # -> 1000  (** is "to the power of")
7 / 2            # -> 3.5
round(3.14159, 2)   # -> 3.14
```

## Functions: a named chunk of code you can reuse
```python
def gallons(dial_difference, fixed_zeros):
    return dial_difference * 10 ** fixed_zeros

gallons(1234, 3)    # -> 1234000
```

## Importing: using code from an add-on or built-in module
```python
import mysql.connector                 # the database connector
from openpyxl import Workbook          # spreadsheets
from datetime import date              # date.today()
import random                          # random.randint(1, 100)
```

## Strings inside strings
```python
"""
    SELECT ...
    FROM ...
"""                # triple quotes let text span several lines - used for SQL
"%" + search + "%"   # + joins text together
```

## Reading error messages
Read the **last line** first, then find the line number it mentions.
- `SyntaxError` - a typo in the Python (missing quote, bracket, colon, or wrong indentation)
- `KeyError: 'nmae'` - you asked a row for a column that is not there (spelling)
- `ProgrammingError ... syntax` - a typo in the SQL, or a column name that clashes with an SQL word
- `Unknown column` - check the spelling against DATABASE_INDEX.md
- `ModuleNotFoundError` - you forgot `source .venv/bin/activate`
