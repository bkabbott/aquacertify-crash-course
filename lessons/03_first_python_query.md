# Lesson 3 - Your first Python query

In lesson 1 you typed SQL into the database command line. Now Python will
do the typing, so you can do something with the answer: print it neatly,
add things up, or put it in a spreadsheet.

## Connecting

Every script starts the same way. Here it is on its own:

`scripts/01_connect.py`
```python
# Connect to the database and prove it worked.
import mysql.connector

conn = mysql.connector.connect(
    host="127.0.0.1",
    user="aquacertify",
    password="aquacertify",
    database="aquacertify",
    charset="utf8mb4",
    collation="utf8mb4_general_ci",
)

cursor = conn.cursor()
cursor.execute("SELECT VERSION()")
print("Connected! Database version:", cursor.fetchone()[0])

conn.close()
```

Run it: `python3 scripts/01_connect.py`
Output:
```
Connected! Database version: 10.11.14-MariaDB-0ubuntu0.24.04.1
```

Line by line:

- `import mysql.connector` - load the add-on that knows how to talk to MariaDB.
- `mysql.connector.connect(...)` - open the door. Same details as `shell.sh`:
  where (`127.0.0.1` means this computer), who, password, which database.
  The last two lines just tell it which alphabet to use; copy them as-is.
- `conn.cursor()` - a cursor is the thing you send questions through.
- `cursor.execute("SELECT VERSION()")` - send a question.
- `cursor.fetchone()` - get one row of the answer. `[0]` picks its first column.
- `conn.close()` - close the door when you are done.

You will retype (or copy) that `connect(...)` block at the top of every
script. It is the same every time.

## The first real question

`scripts/02_first_query.py`
```python
# Your first question: the organizations in the database.
import mysql.connector

conn = mysql.connector.connect(
    host="127.0.0.1", user="aquacertify", password="aquacertify",
    database="aquacertify", charset="utf8mb4", collation="utf8mb4_general_ci",
)
cursor = conn.cursor(dictionary=True)      # dictionary=True: rows come back with column names

cursor.execute("SELECT name, city FROM organizations")
rows = cursor.fetchall()

print(rows)                                 # the raw answer
print()
for row in rows:                            # one row at a time
    print(row["name"], "is in", row["city"])

conn.close()
```

Output:
```
[{'name': 'Consolidated Utilities, Inc.', 'city': 'Savannah'}, {'name': 'Savannah Deluxe Water', 'city': 'Savannah'}]

Consolidated Utilities, Inc. is in Savannah
Savannah Deluxe Water is in Savannah
```

Two new things:

**`cursor(dictionary=True)`** - with this, each row comes back with its
column names attached, so you can say `row["name"]`. Without it you get
plain lists and have to remember that `[0]` is the name. Always use
`dictionary=True`.

**`fetchall()`** - get every row of the answer as a list. The first
`print(rows)` shows the raw list: square brackets around the whole thing,
curly braces around each row. That is the shape of every answer you will
ever get: **a list of rows, each row a dictionary of column -> value**.

The `for` loop then walks through the list, one row at a time. The indented
line runs once per row. That loop is the heart of nearly every script:

1. ask a question - `cursor.execute(...)`
2. get the rows - `cursor.fetchall()`
3. walk through them - `for row in rows:`
4. do something - print / add up / write to a spreadsheet

## A bigger table

`scripts/03_peek_at_wells.py`
```python
# Peek at the first five wells.
import mysql.connector

conn = mysql.connector.connect(
    host="127.0.0.1", user="aquacertify", password="aquacertify",
    database="aquacertify", charset="utf8mb4", collation="utf8mb4_general_ci",
)
cursor = conn.cursor(dictionary=True)

cursor.execute("SELECT name, latitude, longitude FROM wells LIMIT 5")

for row in cursor.fetchall():
    print(row["name"], row["latitude"], row["longitude"])

conn.close()
```

Output:
```
Larchmont 32.022644300000000 -81.236921500000000
Regency 32.032879300000000 -81.254840700000000
Berwick Lakes 32.058115200000000 -81.261527400000000
Enclave 32.041223800000000 -81.239093000000000
Lakes at Cottonvale 32.019629600000000 -81.216289500000000
```

`LIMIT 5` means "just the first five". Notice `for row in cursor.fetchall():`
- you can loop straight over the answer without naming it first.

## Things to try

1. In `03_peek_at_wells.py`, change `LIMIT 5` to `LIMIT 10`. Run it again.
2. Change it to `SELECT * FROM wells LIMIT 3` and print `row` on its own
   (just `print(row)`). See every column.
3. Ask for `SELECT name FROM routes` and print the names.
4. Retype `01_connect.py` from scratch into a new file, `mine.py`, and run
   it. Typos are part of learning: read the last line of the error message.

Next: [Lesson 4 - Asking better questions](04_asking_better_questions.md)
