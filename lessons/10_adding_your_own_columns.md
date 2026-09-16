# Lesson 10 - Adding your own columns

A spreadsheet is not limited to what the database gives you. Once the rows
are in Python you can add **any column you like** before writing them out:
a calculation, a yes/no flag, today's date, a blank for someone to fill in,
a random number. This is where Python earns its keep.

`scripts/19_adding_your_own_columns.py`
```python
# A spreadsheet is not limited to what the database gives you.
# You can add any columns you like: today's date, a calculation, a blank
# column for someone to fill in, a flag, or even a random sample number.
import random
from datetime import date

import mysql.connector
from openpyxl import Workbook
from openpyxl.styles import Font

start = "2026-06-01"
end = "2026-06-30"

conn = mysql.connector.connect(
    host="127.0.0.1", user="aquacertify", password="aquacertify",
    database="aquacertify", charset="utf8mb4", collation="utf8mb4_general_ci",
)
cursor = conn.cursor(dictionary=True)
cursor.execute("""
    SELECT wells.name AS well,
           well_meters.fixed_zeros,
           COUNT(*) AS readings,
           ROUND(AVG(chlorine_residual), 2) AS avg_chlorine,
           MAX(meter_reading) - MIN(meter_reading) AS dial_difference
    FROM well_readings
    JOIN wells       ON wells.id = well_readings.well_id
    JOIN well_meters ON well_meters.id = well_readings.meter_id
    WHERE wells.organization_id = %s AND date_of_reading BETWEEN %s AND %s
      AND well_meters.active = 1
    GROUP BY wells.name, well_meters.fixed_zeros
    ORDER BY wells.name
""", (1, start, end))
rows = cursor.fetchall()
conn.close()

workbook = Workbook()
sheet = workbook.active
sheet.title = "June wells"

# Columns from the database, PLUS columns we invent ourselves:
sheet.append([
    "Well", "Readings", "Avg chlorine",      # straight from the database
    "Gallons",                               # calculated in Python
    "Chlorine OK?",                          # a yes/no flag we decide
    "Report date",                           # today's date
    "Checked by",                            # left blank for a person to fill in
    "Sample #",                              # a random number, e.g. for a spot-check lottery
])

for row in rows:
    gallons = row["dial_difference"] * 10 ** row["fixed_zeros"]
    if row["avg_chlorine"] is not None and row["avg_chlorine"] >= 0.5:
        chlorine_ok = "yes"
    else:
        chlorine_ok = "CHECK"
    sheet.append([
        row["well"], row["readings"], row["avg_chlorine"],
        gallons,
        chlorine_ok,
        date.today(),
        "",
        random.randint(1000, 9999),
    ])

# A total row at the bottom, using a real Excel formula so it updates if someone edits the sheet.
last = sheet.max_row
sheet.append(["TOTAL", "", "", f"=SUM(D2:D{last})"])
sheet.cell(row=sheet.max_row, column=1).font = Font(bold=True)

for cell in sheet[1]:
    cell.font = Font(bold=True)
for r in range(2, sheet.max_row + 1):
    sheet.cell(row=r, column=4).number_format = "#,##0"          # 1,234,567
    sheet.cell(row=r, column=6).number_format = "yyyy-mm-dd"
sheet.column_dimensions["A"].width = 24
sheet.column_dimensions["D"].width = 16

workbook.save("output/june_wells_with_extras.xlsx")
print("Saved output/june_wells_with_extras.xlsx")
```

Output:
```
Saved output/june_wells_with_extras.xlsx
```

Open `output/june_wells_with_extras.xlsx`. Eight columns, only three of
which came straight from the database. Walk through the header list and
the matching `append`:

| Column | Where it comes from |
|---|---|
| Well, Readings, Avg chlorine | the database row, unchanged |
| Gallons | `dial_difference * 10 ** fixed_zeros` - arithmetic in Python |
| Chlorine OK? | an `if`: "yes" when the average is at least 0.5, otherwise "CHECK" |
| Report date | `date.today()` from Python's built-in `datetime` module |
| Checked by | `""` - an empty cell for a person to fill in by hand |
| Sample # | `random.randint(1000, 9999)` - a random four-digit number |

The pattern is always the same: **work out the value in Python, put it in
the list in the right position.** The list you `append` is the row; you
decide what goes in it.

## A live Excel formula

```python
sheet.append(["TOTAL", "", "", f"=SUM(D2:D{last})"])
```

Any cell value that starts with `=` is written as a real Excel formula.
Here `last` is the number of the last data row, so the formula reads
`=SUM(D2:D26)`. If someone edits a gallons figure in Excel, the total
updates - unlike a number Python added up and pasted in. Use a formula
when the reader might change the data; use Python's `sum()` when the
number should be fixed at report time.

## Number formats

```python
sheet.cell(row=r, column=4).number_format = "#,##0"        # 1,234,567
sheet.cell(row=r, column=6).number_format = "yyyy-mm-dd"   # 2026-09-15
```

`sheet.cell(row=..., column=...)` picks one cell by number (row 2, column
4 is D2). `number_format` uses the same codes as Excel's Format Cells
dialog: `"0.00"` for two decimals, `"0%"` for percent, `"$#,##0.00"` for money.

## Why a random column?

It looks like a toy, but "pick some rows at random to double-check" is a
real task - spot-checking readings, choosing addresses for a field audit.
Sort by the Sample # column in Excel and take the top five: that is a
random sample, and nobody can accuse you of cherry-picking. Python's
`random` module also has `random.choice(list)` and `random.shuffle(list)`.

## Things to try

1. Add a column `Days missed` = `30 - row["readings"]`.
2. Change the chlorine rule to flag anything under 0.8.
3. Add a column `Route` (you will need to JOIN routes in the SQL).
4. Make the `CHECK` cells red: `from openpyxl.styles import Font` is
   already imported; set `.font = Font(color="C00000", bold=True)` on that
   cell. Hint: `sheet.cell(row=sheet.max_row, column=5)` right after the append.

Next: [Lesson 11 - The monthly report](11_the_monthly_report.md)
