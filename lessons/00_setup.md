# Lesson 0 - Setting up

You need three things: Python, the database, and two small Python add-ons.
Python and the database are already on this computer. The add-ons are
installed by one script.

## One-time setup

Open a terminal in the course folder and run:

```bash
./setup.sh
```

This creates a folder called `.venv` (a private copy of Python with the
add-ons in it) and installs:

- **mysql-connector-python** - lets Python talk to the database
- **openpyxl** - lets Python write Excel files

## Every time you open a terminal

```bash
cd ~/apps/acertify/aquacertify-crash-course
source .venv/bin/activate
```

The second line switches on the private Python folder. Your prompt will
show `(.venv)` at the start. If you forget this step you will see
`ModuleNotFoundError: No module named 'mysql'` - that is your reminder.

## Check it works

```bash
python3 scripts/01_connect.py
```

You should see:

```
Connected! Database version: 10.11.14-MariaDB-0ubuntu0.24.04.1
```

## How the course works

- `lessons/` - one markdown file per lesson. Read them in order.
- `scripts/` - the Python from each lesson as a file you can run:
  `python3 scripts/05_last_week_of_readings.py`. Every script is short enough
  to retype by hand, and retyping is a good way to learn.
- `output/` - where the spreadsheets you make end up.
- `DATABASE_INDEX.md` - every table and column. Search it (Ctrl+F).
- `PYTHON_BASICS.md` - one page of Python, for when a line looks strange.
- `shell.sh` - opens the database command line (lesson 1).

Nothing in this course changes the database. Every script only reads, so
you can experiment freely.

Next: [Lesson 1 - The database command line](01_the_mariadb_shell.md)
