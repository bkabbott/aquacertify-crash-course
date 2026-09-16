# Builds DATABASE_INDEX.md: every table, what it is for, its columns, and what links to what.
#
#   python3 tools/make_index.py
#
# The database can describe itself (a built-in database called information_schema
# lists every table and column). This script asks it and writes the answer out as
# a document. The only hand-written part is DESCRIPTIONS below.
from collections import defaultdict
from datetime import date

import mysql.connector

DESCRIPTIONS = {
    "Tenancy, users & access": {
        "organizations": "The utility company. Nearly every row in the database belongs to one organization.",
        "states": "US state lookup used by organizations.state_id (currently empty).",
        "companies": "Sub-companies within an organization; used by sli_ga_addresses.company_id.",
        "users": "The people who log in: operators (web), technicians (phone app), and API users. Roles are yes/no columns.",
        "users_routes": "Which routes each user is allowed to work (one row per user/route pair).",
        "route_access_revocations": "A record of route access being taken away from a user.",
        "users_software_meta": "Which app version, phone and OS each user has.",
        "api_credentials": "API key and secret for computer-to-computer access.",
        "verify_email": "One-time codes for verifying an email address.",
        "verify_phone": "One-time codes for verifying a phone number (empty).",
        "verified_numbers": "Phone numbers that passed verification (empty).",
    },
    "Systems, routes & geography": {
        "systems": "A water system, usually one subdivision, with its own drinking water permit.",
        "routes": "A driving route a technician covers. Wells, lift stations and addresses each belong to a route.",
        "ga_counties": "Georgia counties with their FIPS codes (reference data).",
        "aquifers": "Named aquifers, referenced by groundwater withdrawal permits.",
        "treatment_plants": "Water treatment plants.",
        "elevated_tanks": "Elevated storage tanks (empty).",
    },
    "Permits": {
        "safe_drinking_water_permits": "Safe Drinking Water Act permit numbers; each system links to one.",
        "groundwater_withdrawal_permits": "Permits to pump groundwater; links an organization, a system and an aquifer.",
    },
    "Wells (groundwater production)": {
        "wells": "The wells, with GPS coordinates, route, system, and permit.",
        "well_meters": "The flow meter on each well. moving_digits / fixed_zeros describe the dial.",
        "well_readings": "One row per day per well: the meter dial, the chlorine level, who read it. The biggest table.",
    },
    "Lift stations (wastewater)": {
        "lift_stations": "Wastewater pumping stations, with GPS coordinates, route and system.",
        "lift_station_dials": "The hour-meter dials on a lift station's pumps (pump 1 and pump 2).",
        "station_readings": "One row per day per station: both pump dials plus rainfall. Second biggest table.",
    },
    "Customer meters": {
        "customer_meters": "Customer water meters, keyed by harmony_meter_id / serial_number (from billing).",
        "meters_sli_ga_addresses": "Which customer meter is at which inventory address.",
    },
    "Service Line Inventory - Georgia (sli_ga_*)": {
        "sli_ga_addresses": "Every customer address in the Georgia lead service line inventory.",
        "sli_ga_addresses_meta": "Property type / land use for an address.",
        "sli_ga_neighborhoods": "Neighborhood names within a route.",
        "sli_ga_subdivisions": "Subdivision names.",
        "sli_ga_service_lines": "One row per service line at an address: materials, how they were determined, and the overall lead verdict. Most *_id columns point at a *_responses table.",
        "sli_ga_photos": "Photos of service lines uploaded to S3, with GPS.",
        "sli_ga_basis_of_classification_responses": "Multiple-choice answers: how a material was determined.",
        "sli_ga_building_type_responses": "Multiple-choice answers: building type.",
        "sli_ga_customer_owned_material_responses": "Multiple-choice answers: customer-side material category.",
        "sli_ga_overall_service_line_classification_responses": "Multiple-choice answers: Lead / Non-Lead / GRR / GNRR / Unknown.",
        "sli_ga_presence_of_lead_connector_responses": "Multiple-choice answers: lead connector present?",
        "sli_ga_school_or_childcare_facility_responses": "Multiple-choice answers: school or childcare?",
        "sli_ga_service_line_installation_date_responses": "Multiple-choice answers: when it was installed.",
        "sli_ga_service_line_ownership_type_responses": "Multiple-choice answers: who owns the line.",
        "sli_ga_specific_service_line_material_responses": "Multiple-choice answers: the exact material (Copper, PVC, ...).",
        "sli_ga_system_owned_material_responses": "Multiple-choice answers: system-side material category.",
    },
    "Service Line Inventory - generic (sli_*)": {
        "sli_locations": "Older inventory location records.",
        "sli_neighborhoods": "Neighborhood lookup for sli_locations.",
        "sli_service_lines": "Older service line records (empty).",
        "sli_curb_stops": "Curb stop records (empty).",
        "sli_water_mains": "Water main records (empty).",
        "sli_service_line_diameter": "Multiple-choice answers: pipe diameter.",
        "sli_water_main_materials": "Multiple-choice answers: water main material.",
        "sli_building_plumbing_lead_solder_responses": "Multiple-choice answers: lead solder in the building?",
        "sli_curb_stop_materials_responses": "Multiple-choice answers: curb stop material.",
        "sli_customer_owned_classification_basis_responses": "Multiple-choice answers: basis for customer-side classification.",
        "sli_fittings_verification_method_responses": "Multiple-choice answers: how fittings were checked.",
        "sli_installed_after_lead_ban_responses": "Multiple-choice answers: installed after the lead ban?",
        "sli_lcr_sampling_site_responses": "Multiple-choice answers: Lead & Copper Rule sampling site?",
        "sli_lcr_tier_responses": "Multiple-choice answers: LCR sampling tier.",
        "sli_point_of_entry_responses": "Multiple-choice answers: point-of-entry treatment.",
        "sli_property_classification_responses": "Multiple-choice answers: property classification.",
        "sli_sensitive_population_responses": "Multiple-choice answers: sensitive population served?",
        "sli_service_line_materials_responses": "Multiple-choice answers: service line material.",
        "sli_system_owned_classification_basis_responses": "Multiple-choice answers: basis for system-side classification.",
    },
    "Operations & diagnostics": {
        "errors": "A log of errors from the phone/web app: what was sent, which page, what went wrong, when.",
    },
}
TABLE_TO_GROUP = {t: g for g, tables in DESCRIPTIONS.items() for t in tables}

conn = mysql.connector.connect(
    host="127.0.0.1", user="aquacertify", password="aquacertify",
    database="aquacertify", charset="utf8mb4", collation="utf8mb4_general_ci",
)
cursor = conn.cursor(dictionary=True)

cursor.execute("""
    SELECT TABLE_NAME AS name FROM information_schema.TABLES
    WHERE TABLE_SCHEMA = DATABASE() ORDER BY TABLE_NAME""")
tables = [r["name"] for r in cursor.fetchall()]

cursor.execute("""
    SELECT TABLE_NAME AS tbl, COLUMN_NAME AS col, COLUMN_TYPE AS type, IS_NULLABLE AS nullable, COLUMN_KEY AS keytype
    FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = DATABASE()
    ORDER BY TABLE_NAME, ORDINAL_POSITION""")
columns = defaultdict(list)
for c in cursor.fetchall():
    columns[c["tbl"]].append(c)

cursor.execute("""
    SELECT TABLE_NAME AS tbl, COLUMN_NAME AS col, REFERENCED_TABLE_NAME AS ref_tbl, REFERENCED_COLUMN_NAME AS ref_col
    FROM information_schema.KEY_COLUMN_USAGE
    WHERE TABLE_SCHEMA = DATABASE() AND REFERENCED_TABLE_NAME IS NOT NULL
    ORDER BY TABLE_NAME, COLUMN_NAME""")
links_out, links_in, seen = defaultdict(list), defaultdict(list), set()
for f in cursor.fetchall():
    key = (f["tbl"], f["col"], f["ref_tbl"])
    if key not in seen:
        seen.add(key)
        links_out[f["tbl"]].append(f)
        links_in[f["ref_tbl"]].append(f)

rows_in = {}
for t in tables:
    cursor.execute(f"SELECT COUNT(*) AS n FROM `{t}`")
    rows_in[t] = cursor.fetchone()["n"]
conn.close()

out = []
out.append("# AquaCertify Database Index\n")
out.append(f"Every table in our database ({len(tables)} of them), what each one is for, its columns, "
           f"and what links to what. Generated {date.today()} by `python3 tools/make_index.py`.\n")
out.append('Tip: use your editor\'s search (Ctrl+F) to find a column, e.g. "chlorine".\n')

out.append("## Groups at a glance\n")
out.append("| Group | Tables | Total rows |\n|---|---|---|")
for group, tbls in DESCRIPTIONS.items():
    present = [t for t in tbls if t in rows_in]
    out.append(f"| {group} | {len(present)} | {sum(rows_in[t] for t in present):,} |")
out.append("")
out.append("## How the main tables connect\n")
out.append("""```
organizations ──< users ──< users_routes >── routes
      │                                        │
      ├──< systems ──< wells ──< well_meters ──< well_readings
      │        │         └── route_id ─────────┘
      │        └──< lift_stations ──< lift_station_dials ──< station_readings
      │
      ├──< safe_drinking_water_permits ── systems
      ├──< groundwater_withdrawal_permits ── aquifers, wells
      │
      └──< sli_ga_addresses ──< sli_ga_service_lines ──< sli_ga_photos
                 │  (route, system, neighborhood,   └── *_responses (multiple-choice answers)
                 │   subdivision, company, meter)
                 └──< meters_sli_ga_addresses >── customer_meters
```
""")
out.append("## All tables\n")
out.append("| Table | Group | Rows | What it is |\n|---|---|---:|---|")
for t in tables:
    group = TABLE_TO_GROUP.get(t, "(other)")
    out.append(f"| [`{t}`](#{t}) | {group} | {rows_in[t]:,} | {DESCRIPTIONS.get(group, {}).get(t, '')} |")
out.append("")
out.append("## Table details")
groups = list(DESCRIPTIONS.items())
other = [t for t in tables if t not in TABLE_TO_GROUP]
if other:
    groups.append(("(other)", {t: "" for t in other}))
for group, tbls in groups:
    out.append(f"\n### {group}")
    for t, what in tbls.items():
        if t not in rows_in:
            continue
        out.append(f"\n#### `{t}`\n")
        if what:
            out.append(what + "\n")
        out.append(f"Rows: {rows_in[t]:,}\n")
        out.append("| Column | Type | Can be empty | Key |\n|---|---|---|---|")
        for c in columns[t]:
            out.append(f"| {c['col']} | {c['type']} | {c['nullable']} | {c['keytype']} |")
        if links_out[t]:
            out.append("\nLinks to: " + ", ".join(f"`{f['col']}` → `{f['ref_tbl']}.{f['ref_col']}`" for f in links_out[t]))
        if links_in[t]:
            out.append("\nLinked from: " + ", ".join(f"`{f['tbl']}.{f['col']}`" for f in links_in[t]))

with open("DATABASE_INDEX.md", "w", encoding="utf-8") as fh:
    fh.write("\n".join(out) + "\n")
print(f"Wrote DATABASE_INDEX.md ({len(tables)} tables)")
