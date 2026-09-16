# Lesson 1 - The database command line

Before any Python, meet the database directly. MariaDB (the database
program) comes with a command line where you type a question and it prints
the answer. It is the fastest way to look around.

## Opening it

```bash
./shell.sh
```

(That runs `mariadb -u aquacertify -paquacertify aquacertify` for you:
the program, the username, the password, and which database.)

You will see a prompt:

```
MariaDB [aquacertify]>
```

Every command ends with a semicolon `;` and then Enter. If you press Enter
without a semicolon it just waits for more - type `;` and Enter to finish.
To leave, type `exit` and Enter.

## What tables are there?

```sql
SHOW TABLES;
```

```
+------------------------------------------------------+
| Tables_in_aquacertify                                |
+------------------------------------------------------+
| api_credentials                                      |
| aquifers                                             |
| companies                                            |
| customer_meters                                      |
| elevated_tanks                                       |
| errors                                               |
| ga_counties                                          |
...
63 rows in set
```

A table is like a spreadsheet: columns across the top, one row per thing.

## What columns does a table have?

```sql
DESCRIBE wells;
```

```
+----------------------------------+----------------+------+-----+---------+----------------+
| Field                            | Type           | Null | Key | Default | Extra          |
+----------------------------------+----------------+------+-----+---------+----------------+
| id                               | mediumint(8)   | NO   | PRI | NULL    | auto_increment |
| name                             | varchar(45)    | NO   | MUL | NULL    |                |
| latitude                         | decimal(17,15) | YES  |     | NULL    |                |
| longitude                        | decimal(18,15) | YES  |     | NULL    |                |
| route_id                         | mediumint(8)   | NO   | MUL | NULL    |                |
| organization_id                  | mediumint(8)   | NO   | MUL | NULL    |                |
| system_id                        | mediumint(8)   | NO   | MUL | NULL    |                |
| created                          | datetime       | NO   |     | NULL    |                |
| modified                         | datetime       | NO   |     | NULL    |                |
| groundwater_withdrawal_permit_id | int(11)        | YES  | MUL | NULL    |                |
| source_number                    | varchar(9)     | NO   |     | NULL    |                |
| plant_number                     | char(3)        | NO   |     | NULL    |                |
+----------------------------------+----------------+------+-----+---------+----------------+
```

`Field` is the column name. `Type` says what kind of thing it holds:
`varchar` = text, `int`/`mediumint` = whole number, `decimal` = number with
a decimal point, `date`/`datetime` = a date. `Key = PRI` marks the `id`
column that gives each row its number.

## Looking at some rows

```sql
SELECT id, name, route_id FROM wells LIMIT 3;
```

```
+----+---------------+----------+
| id | name          | route_id |
+----+---------------+----------+
| 21 | Larchmont     |        1 |
| 22 | Regency       |        1 |
| 23 | Berwick Lakes |        1 |
+----+---------------+----------+
```

Read it out loud: "SELECT the id, name and route_id FROM wells, LIMIT 3
rows." That is SQL, and it is the same language you will use from Python.

`SELECT * FROM wells LIMIT 3;` shows all columns (`*` = everything).

## How big is a table?

```sql
SELECT COUNT(*) FROM well_readings;
```

```
+----------+
| COUNT(*) |
+----------+
|    69853 |
+----------+
```

## Which way do the tables link?

```sql
SHOW CREATE TABLE routes\G
```

(`\G` instead of `;` prints it sideways so long lines are readable.)

```
CREATE TABLE `routes` (
  `id` mediumint(8) NOT NULL AUTO_INCREMENT,
  `name` varchar(21) NOT NULL,
  `organization_id` mediumint(8) NOT NULL,
  ...
  CONSTRAINT `routes_ibfk_1` FOREIGN KEY (`organization_id`) REFERENCES `organizations` (`id`)
)
```

The `FOREIGN KEY` line says: `routes.organization_id` holds the `id` of a
row in `organizations`. That is how tables link - a column holding another
table's id number. `DATABASE_INDEX.md` lists all of these links for you.

## Things to try

1. `DESCRIBE well_readings;` - find the chlorine column.
2. `SELECT * FROM routes;` - all of them fit on one screen.
3. `SELECT name FROM wells WHERE route_id = 4;` - only route 4.
4. `SELECT * FROM well_readings ORDER BY date_of_reading DESC LIMIT 5;` - the five newest readings.
5. Forget the semicolon on purpose, see what happens, then type `;`.

## Cheat sheet

| Want to... | Type |
|---|---|
| list tables | `SHOW TABLES;` |
| see a table's columns | `DESCRIBE tablename;` |
| see how a table was built, with links | `SHOW CREATE TABLE tablename\G` |
| peek at rows | `SELECT * FROM tablename LIMIT 5;` |
| count rows | `SELECT COUNT(*) FROM tablename;` |
| leave | `exit` |

Next: [Lesson 2 - What is in our database](02_what_is_in_the_database.md)
