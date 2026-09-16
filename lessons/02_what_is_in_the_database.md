# Lesson 2 - What is in our database

## The story

A water utility (an **organization**) runs a number of small water
**systems** - typically one per subdivision. Each system gets its water
from one or more **wells**. Every well has a **meter** with a dial on it,
like a car's odometer: it only counts up.

Every day, **technicians** drive their **routes**, stop at each well, look
at the dial, test the chlorine, and type the numbers into the phone app.
That becomes one row in **well_readings**. They do the same at each
**lift station** (a wastewater pump) and that becomes a row in
**station_readings** - along with how much it rained.

Separately, the state requires an inventory of what every customer's water
pipe is made of, to find any lead. Those are the **sli_ga_** tables
(Service Line Inventory, Georgia).

**Operators** in the office look at all of this to answer questions like
"how many gallons did we pump last month?" - which is what you will learn
to do.

## The tables that matter most

There are 63 tables. These fourteen are the ones you will use:

| Table | Rows | What it is |
|---|---:|---|
| `organizations` | 2 | The company. (#2 is a practice copy of #1.) |
| `users` | 27 | The people. Operators, technicians, and one API user. |
| `routes` | 8 | Driving routes: Larchmont, Effingham, Islands, Black Creek (x2 orgs). |
| `systems` | 30 | Water systems, usually one subdivision each. |
| `wells` | 50 | The wells, with GPS coordinates. |
| `well_meters` | 84 | The meter on each well and how to read its dial. |
| `well_readings` | 69,853 | One row per well per day: dial reading + chlorine. |
| `lift_stations` | 50 | Wastewater pumping stations. |
| `lift_station_dials` | 50 | The hour-meter on each of the two pumps. |
| `station_readings` | 62,101 | One row per station per day: both pump dials + rainfall. |
| `sli_ga_addresses` | 16,927 | Customer addresses in the lead inventory. |
| `sli_ga_service_lines` | 16,434 | For each address: pipe material and lead verdict. |
| `customer_meters` | 8,309 | Customer water meters. |
| `errors` | 270 | Things that went wrong in the app. |

## How they link together

```
organization
   |
   +-- users ---- (users_routes) ---- routes
   |                                     |
   +-- systems --- wells --- well_meters --- well_readings
   |                 |
   |                 +--- lift_stations --- lift_station_dials --- station_readings
   |
   +-- sli_ga_addresses --- sli_ga_service_lines
```

Each line is a link. A well row has a column `route_id` holding the
*number* of its route. To see the route's *name* you look it up in the
routes table. Lesson 5 shows how to do that in one go.

## Two organizations

Organization 1 is the real company. Organization 2 is a near-identical copy
used for practice and demos. When you write a question, add
`WHERE organization_id = 1` so you are looking at the real one. You will
see that in almost every script.

## Where to look things up

`DATABASE_INDEX.md` lists all 63 tables, every column, and what links to
what. Keep it open next to you. When you wonder "where would the chlorine
number be?", search that file for "chlorine".

You can also ask the database itself, from the command line in lesson 1:
`DESCRIBE well_readings;`

Next: [Lesson 3 - Your first Python query](03_first_python_query.md)
