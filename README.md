# aquacertify-crash-course
I told Claude this.

❯ Use local mariadb connection user aquacertify password aquacertify. Make an index of which tables exist in our database, and construct a course using Python and a MySQL connector that goes into different uses of our data.
This course should prepare someone to know which tables exist in the db, as well as teach fundamental software engineering paradigms.

---


**A gentle introduction to our database, and to using Python to ask it
questions and turn the answers into spreadsheets.** No programming
experience needed.

## What this is about

Our company runs water systems. Every day, technicians drive their routes,
stop at each well and lift station, read the meters, test the chlorine,
and type the numbers into an app. All of that lands in a database.

A database is just a collection of tables, and a table is just a
spreadsheet: columns across the top, one row per thing. Ours has 63 tables -
wells, meter readings, lift stations, rainfall, the people, the lead pipe
inventory, and more.

The magic is that you can *ask the database questions* and get answers in
a blink: "How many gallons did we pump in June?" "Which well had the lowest
chlorine this week?" "Does rain make the sewer pumps work harder?" (It
does - lesson 7 proves it.) This course teaches you how, and by the end you
will be producing a real Excel report straight from the data.

## Start here

1. Run `./setup.sh` once.
2. Each time you open a terminal: `source .venv/bin/activate`
3. Read `lessons/00_setup.md`, then work through the lessons in order.

## The lessons

Each lesson is a markdown file you read. The Python in it is also in
`scripts/`, ready to run - and short enough to retype, which is the best
way to learn.

| Lesson | What you learn | Scripts |
|---|---|---|
| [0 - Setup](lessons/00_setup.md) | getting Python and the add-ons ready | |
| [1 - The database command line](lessons/01_the_mariadb_shell.md) | `SHOW TABLES`, `DESCRIBE`, `SELECT` straight into MariaDB | `shell.sh` |
| [2 - What is in our database](lessons/02_what_is_in_the_database.md) | the story the tables tell, and the map | |
| [3 - Your first Python query](lessons/03_first_python_query.md) | connect, ask, loop over the answer | 01-03 |
| [4 - Asking better questions](lessons/04_asking_better_questions.md) | WHERE, ORDER BY, LIMIT, LIKE, and `%s` blanks | 04-06 |
| [5 - Connecting tables](lessons/05_connecting_tables.md) | JOIN: id numbers become names | 07-08 |
| [6 - Counting and totals](lessons/06_counting_and_totals.md) | COUNT / AVG / MIN / MAX, GROUP BY, gallons pumped | 09-11 |
| [7 - Rain and pumps](lessons/07_rain_and_pumps.md) | a real discovery hiding in the lift station data | 12-13 |
| [8 - The lead pipe inventory](lessons/08_the_lead_pipe_inventory.md) | multiple-choice tables, a report for the state | 14-16 |
| [9 - Your first spreadsheet](lessons/09_your_first_spreadsheet.md) | openpyxl: rows in, .xlsx out, bold headers | 17-18 |
| [10 - Adding your own columns](lessons/10_adding_your_own_columns.md) | calculations, flags, today's date, blanks, random numbers, formulas | 19 |
| [11 - The monthly report](lessons/11_the_monthly_report.md) | three tabs and a chart in one file | 20 |
| [12 - Cookbook and next steps](lessons/12_cookbook_and_next_steps.md) | nine ready-made questions, a template, and what errors mean | 21 |

## What is in this folder

```
lessons/            the course - read these in order
scripts/            every Python example, numbered to match the lessons
output/             spreadsheets you make land here
shell.sh            opens the MariaDB command line, already logged in
DATABASE_INDEX.md   every table, every column, what links to what (search it)
PYTHON_BASICS.md    one page of Python for when a line looks strange
tools/make_index.py rebuilds DATABASE_INDEX.md from the live database
setup.sh            one-time setup
```

## Running a script

Always from this folder (not from inside `scripts/`), with the venv on:

```bash
source .venv/bin/activate
python3 scripts/10_gallons_in_june.py
```

## Safety

Every script and every lesson only *reads* from the database. Nothing here
changes, adds or deletes data, so you cannot break anything by experimenting.
