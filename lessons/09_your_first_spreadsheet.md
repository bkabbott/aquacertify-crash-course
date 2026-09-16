# Lesson 9 - Your first spreadsheet

Printing to the screen is fine for you. For anyone else - your dad, the
office, the state - the answer needs to be a spreadsheet. **openpyxl** is
the add-on that writes real `.xlsx` files, and the idea is very simple:

1. make a `Workbook` (the file)
2. `append` one list per row to a sheet
3. `save` it

## The simplest possible spreadsheet

`scripts/17_first_spreadsheet.py`
```python
# The simplest possible spreadsheet: the list of wells.
import mysql.connector
from openpyxl import Workbook

conn = mysql.connector.connect(
    host="127.0.0.1", user="aquacertify", password="aquacertify",
    database="aquacertify", charset="utf8mb4", collation="utf8mb4_general_ci",
)
cursor = conn.cursor(dictionary=True)
cursor.execute("""
    SELECT wells.name AS well, routes.name AS route, wells.latitude, wells.longitude
    FROM wells
    JOIN routes ON routes.id = wells.route_id
    WHERE wells.organization_id = %s
    ORDER BY routes.name, wells.name
""", (1,))
rows = cursor.fetchall()
conn.close()

workbook = Workbook()                       # a new, empty spreadsheet file
sheet = workbook.active                     # its first tab
sheet.title = "Wells"

sheet.append(["Well", "Route", "Latitude", "Longitude"])       # row 1: the headers
for row in rows:
    sheet.append([row["well"], row["route"], row["latitude"], row["longitude"]])

workbook.save("output/wells.xlsx")
print(f"Saved output/wells.xlsx with {len(rows)} wells")
```

Output:
```
Saved output/wells.xlsx with 25 wells
```

Open `output/wells.xlsx` in Excel or LibreOffice. The top half of the
script is lesson 5's JOIN; the bottom half is new:

- `Workbook()` - a new, empty spreadsheet file in memory.
- `workbook.active` - its first tab. `sheet.title` names the tab.
- `sheet.append([...])` - adds one row. The first append is the header
  row; then the loop appends one row per database row.
- `workbook.save("output/wells.xlsx")` - write the file.

Note the order inside `append`: a plain list of values,
`[row["well"], row["route"], ...]`, in the same order as the headers.
That is the one thing to get right.

Notice also `conn.close()` moved up: we fetched the rows into `rows` and
closed the database *before* building the spreadsheet. Get the data, close
the door, then work with what you have.

## Making it presentable

`scripts/18_spreadsheet_with_style.py`
```python
# The same list, but with bold headers, sensible column widths and a frozen header row.
import mysql.connector
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

conn = mysql.connector.connect(
    host="127.0.0.1", user="aquacertify", password="aquacertify",
    database="aquacertify", charset="utf8mb4", collation="utf8mb4_general_ci",
)
cursor = conn.cursor(dictionary=True)
cursor.execute("""
    SELECT wells.name AS well, routes.name AS route, wells.latitude, wells.longitude
    FROM wells
    JOIN routes ON routes.id = wells.route_id
    WHERE wells.organization_id = %s
    ORDER BY routes.name, wells.name
""", (1,))
rows = cursor.fetchall()
conn.close()

workbook = Workbook()
sheet = workbook.active
sheet.title = "Wells"

sheet.append(["Well", "Route", "Latitude", "Longitude"])
for row in rows:
    sheet.append([row["well"], row["route"], row["latitude"], row["longitude"]])

# --- styling -------------------------------------------------------------
for cell in sheet[1]:                                   # every cell in row 1
    cell.font = Font(bold=True, color="FFFFFF")         # white bold text
    cell.fill = PatternFill("solid", fgColor="1F4E78")  # dark blue background

sheet.column_dimensions["A"].width = 24
sheet.column_dimensions["B"].width = 14
sheet.column_dimensions["C"].width = 12
sheet.column_dimensions["D"].width = 12

sheet.freeze_panes = "A2"                               # headers stay put when you scroll

workbook.save("output/wells_styled.xlsx")
print("Saved output/wells_styled.xlsx")
```

Output:
```
Saved output/wells_styled.xlsx
```

Everything above the `# --- styling` line is identical to before. Below it:

- `sheet[1]` is row 1 (the headers). The loop sets each cell's `font`
  and `fill`. Colours are written as six hex digits - `1F4E78` is dark blue,
  `FFFFFF` is white. Any web colour picker gives you these.
- `column_dimensions["A"].width` sets a column's width. Columns are
  lettered like in Excel.
- `freeze_panes = "A2"` keeps row 1 visible when you scroll.

That is 90% of the formatting anyone ever asks for.

## Things to try

1. Add a `Latitude`/`Longitude`-free version: only well and route.
2. Change the header colour to green (`00875A`).
3. Add a fourth column `System` by extending the JOIN
   (`JOIN systems ON systems.id = wells.system_id`, then `systems.name AS system_name`).
4. Sort by well name instead of route.

Next: [Lesson 10 - Adding your own columns](10_adding_your_own_columns.md)
