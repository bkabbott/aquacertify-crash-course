# AquaCertify Database Index

Every table in our database (63 of them), what each one is for, its columns, and what links to what. Generated 2026-09-15 by `python3 tools/make_index.py`.

Tip: use your editor's search (Ctrl+F) to find a column, e.g. "chlorine".

## Groups at a glance

| Group | Tables | Total rows |
|---|---|---|
| Tenancy, users & access | 11 | 170 |
| Systems, routes & geography | 6 | 231 |
| Permits | 2 | 55 |
| Wells (groundwater production) | 3 | 69,987 |
| Lift stations (wastewater) | 3 | 62,201 |
| Customer meters | 2 | 8,609 |
| Service Line Inventory - Georgia (sli_ga_*) | 16 | 35,406 |
| Service Line Inventory - generic (sli_*) | 19 | 8,091 |
| Operations & diagnostics | 1 | 270 |

## How the main tables connect

```
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

## All tables

| Table | Group | Rows | What it is |
|---|---|---:|---|
| [`api_credentials`](#api_credentials) | Tenancy, users & access | 1 | API key and secret for computer-to-computer access. |
| [`aquifers`](#aquifers) | Systems, routes & geography | 31 | Named aquifers, referenced by groundwater withdrawal permits. |
| [`companies`](#companies) | Tenancy, users & access | 6 | Sub-companies within an organization; used by sli_ga_addresses.company_id. |
| [`customer_meters`](#customer_meters) | Customer meters | 7,954 | Customer water meters, keyed by harmony_meter_id / serial_number (from billing). |
| [`elevated_tanks`](#elevated_tanks) | Systems, routes & geography | 1 | Elevated storage tanks (empty). |
| [`errors`](#errors) | Operations & diagnostics | 270 | A log of errors from the phone/web app: what was sent, which page, what went wrong, when. |
| [`ga_counties`](#ga_counties) | Systems, routes & geography | 159 | Georgia counties with their FIPS codes (reference data). |
| [`groundwater_withdrawal_permits`](#groundwater_withdrawal_permits) | Permits | 10 | Permits to pump groundwater; links an organization, a system and an aquifer. |
| [`lift_stations`](#lift_stations) | Lift stations (wastewater) | 50 | Wastewater pumping stations, with GPS coordinates, route and system. |
| [`lift_station_dials`](#lift_station_dials) | Lift stations (wastewater) | 50 | The hour-meter dials on a lift station's pumps (pump 1 and pump 2). |
| [`meters_sli_ga_addresses`](#meters_sli_ga_addresses) | Customer meters | 655 | Which customer meter is at which inventory address. |
| [`organizations`](#organizations) | Tenancy, users & access | 2 | The utility company. Nearly every row in the database belongs to one organization. |
| [`routes`](#routes) | Systems, routes & geography | 8 | A driving route a technician covers. Wells, lift stations and addresses each belong to a route. |
| [`route_access_revocations`](#route_access_revocations) | Tenancy, users & access | 0 | A record of route access being taken away from a user. |
| [`safe_drinking_water_permits`](#safe_drinking_water_permits) | Permits | 45 | Safe Drinking Water Act permit numbers; each system links to one. |
| [`sli_building_plumbing_lead_solder_responses`](#sli_building_plumbing_lead_solder_responses) | Service Line Inventory - generic (sli_*) | 3 | Multiple-choice answers: lead solder in the building? |
| [`sli_curb_stops`](#sli_curb_stops) | Service Line Inventory - generic (sli_*) | 0 | Curb stop records (empty). |
| [`sli_curb_stop_materials_responses`](#sli_curb_stop_materials_responses) | Service Line Inventory - generic (sli_*) | 17 | Multiple-choice answers: curb stop material. |
| [`sli_customer_owned_classification_basis_responses`](#sli_customer_owned_classification_basis_responses) | Service Line Inventory - generic (sli_*) | 23 | Multiple-choice answers: basis for customer-side classification. |
| [`sli_fittings_verification_method_responses`](#sli_fittings_verification_method_responses) | Service Line Inventory - generic (sli_*) | 19 | Multiple-choice answers: how fittings were checked. |
| [`sli_ga_addresses`](#sli_ga_addresses) | Service Line Inventory - Georgia (sli_ga_*) | 16,954 | Every customer address in the Georgia lead service line inventory. |
| [`sli_ga_addresses_meta`](#sli_ga_addresses_meta) | Service Line Inventory - Georgia (sli_ga_*) | 29 | Property type / land use for an address. |
| [`sli_ga_basis_of_classification_responses`](#sli_ga_basis_of_classification_responses) | Service Line Inventory - Georgia (sli_ga_*) | 9 | Multiple-choice answers: how a material was determined. |
| [`sli_ga_building_type_responses`](#sli_ga_building_type_responses) | Service Line Inventory - Georgia (sli_ga_*) | 5 | Multiple-choice answers: building type. |
| [`sli_ga_customer_owned_material_responses`](#sli_ga_customer_owned_material_responses) | Service Line Inventory - Georgia (sli_ga_*) | 6 | Multiple-choice answers: customer-side material category. |
| [`sli_ga_neighborhoods`](#sli_ga_neighborhoods) | Service Line Inventory - Georgia (sli_ga_*) | 118 | Neighborhood names within a route. |
| [`sli_ga_overall_service_line_classification_responses`](#sli_ga_overall_service_line_classification_responses) | Service Line Inventory - Georgia (sli_ga_*) | 5 | Multiple-choice answers: Lead / Non-Lead / GRR / GNRR / Unknown. |
| [`sli_ga_photos`](#sli_ga_photos) | Service Line Inventory - Georgia (sli_ga_*) | 8 | Photos of service lines uploaded to S3, with GPS. |
| [`sli_ga_presence_of_lead_connector_responses`](#sli_ga_presence_of_lead_connector_responses) | Service Line Inventory - Georgia (sli_ga_*) | 3 | Multiple-choice answers: lead connector present? |
| [`sli_ga_school_or_childcare_facility_responses`](#sli_ga_school_or_childcare_facility_responses) | Service Line Inventory - Georgia (sli_ga_*) | 4 | Multiple-choice answers: school or childcare? |
| [`sli_ga_service_lines`](#sli_ga_service_lines) | Service Line Inventory - Georgia (sli_ga_*) | 16,926 | One row per service line at an address: materials, how they were determined, and the overall lead verdict. Most *_id columns point at a *_responses table. |
| [`sli_ga_service_line_installation_date_responses`](#sli_ga_service_line_installation_date_responses) | Service Line Inventory - Georgia (sli_ga_*) | 3 | Multiple-choice answers: when it was installed. |
| [`sli_ga_service_line_ownership_type_responses`](#sli_ga_service_line_ownership_type_responses) | Service Line Inventory - Georgia (sli_ga_*) | 4 | Multiple-choice answers: who owns the line. |
| [`sli_ga_specific_service_line_material_responses`](#sli_ga_specific_service_line_material_responses) | Service Line Inventory - Georgia (sli_ga_*) | 14 | Multiple-choice answers: the exact material (Copper, PVC, ...). |
| [`sli_ga_subdivisions`](#sli_ga_subdivisions) | Service Line Inventory - Georgia (sli_ga_*) | 1,312 | Subdivision names. |
| [`sli_ga_system_owned_material_responses`](#sli_ga_system_owned_material_responses) | Service Line Inventory - Georgia (sli_ga_*) | 6 | Multiple-choice answers: system-side material category. |
| [`sli_installed_after_lead_ban_responses`](#sli_installed_after_lead_ban_responses) | Service Line Inventory - generic (sli_*) | 3 | Multiple-choice answers: installed after the lead ban? |
| [`sli_lcr_sampling_site_responses`](#sli_lcr_sampling_site_responses) | Service Line Inventory - generic (sli_*) | 3 | Multiple-choice answers: Lead & Copper Rule sampling site? |
| [`sli_lcr_tier_responses`](#sli_lcr_tier_responses) | Service Line Inventory - generic (sli_*) | 5 | Multiple-choice answers: LCR sampling tier. |
| [`sli_locations`](#sli_locations) | Service Line Inventory - generic (sli_*) | 7,856 | Older inventory location records. |
| [`sli_neighborhoods`](#sli_neighborhoods) | Service Line Inventory - generic (sli_*) | 36 | Neighborhood lookup for sli_locations. |
| [`sli_point_of_entry_responses`](#sli_point_of_entry_responses) | Service Line Inventory - generic (sli_*) | 3 | Multiple-choice answers: point-of-entry treatment. |
| [`sli_property_classification_responses`](#sli_property_classification_responses) | Service Line Inventory - generic (sli_*) | 14 | Multiple-choice answers: property classification. |
| [`sli_sensitive_population_responses`](#sli_sensitive_population_responses) | Service Line Inventory - generic (sli_*) | 7 | Multiple-choice answers: sensitive population served? |
| [`sli_service_lines`](#sli_service_lines) | Service Line Inventory - generic (sli_*) | 0 | Older service line records (empty). |
| [`sli_service_line_diameter`](#sli_service_line_diameter) | Service Line Inventory - generic (sli_*) | 18 | Multiple-choice answers: pipe diameter. |
| [`sli_service_line_materials_responses`](#sli_service_line_materials_responses) | Service Line Inventory - generic (sli_*) | 26 | Multiple-choice answers: service line material. |
| [`sli_system_owned_classification_basis_responses`](#sli_system_owned_classification_basis_responses) | Service Line Inventory - generic (sli_*) | 31 | Multiple-choice answers: basis for system-side classification. |
| [`sli_water_mains`](#sli_water_mains) | Service Line Inventory - generic (sli_*) | 0 | Water main records (empty). |
| [`sli_water_main_materials`](#sli_water_main_materials) | Service Line Inventory - generic (sli_*) | 27 | Multiple-choice answers: water main material. |
| [`states`](#states) | Tenancy, users & access | 1 | US state lookup used by organizations.state_id (currently empty). |
| [`station_readings`](#station_readings) | Lift stations (wastewater) | 62,101 | One row per day per station: both pump dials plus rainfall. Second biggest table. |
| [`systems`](#systems) | Systems, routes & geography | 30 | A water system, usually one subdivision, with its own drinking water permit. |
| [`treatment_plants`](#treatment_plants) | Systems, routes & geography | 2 | Water treatment plants. |
| [`users`](#users) | Tenancy, users & access | 27 | The people who log in: operators (web), technicians (phone app), and API users. Roles are yes/no columns. |
| [`users_routes`](#users_routes) | Tenancy, users & access | 104 | Which routes each user is allowed to work (one row per user/route pair). |
| [`users_software_meta`](#users_software_meta) | Tenancy, users & access | 17 | Which app version, phone and OS each user has. |
| [`verified_numbers`](#verified_numbers) | Tenancy, users & access | 1 | Phone numbers that passed verification (empty). |
| [`verify_email`](#verify_email) | Tenancy, users & access | 11 | One-time codes for verifying an email address. |
| [`verify_phone`](#verify_phone) | Tenancy, users & access | 0 | One-time codes for verifying a phone number (empty). |
| [`wells`](#wells) | Wells (groundwater production) | 50 | The wells, with GPS coordinates, route, system, and permit. |
| [`well_meters`](#well_meters) | Wells (groundwater production) | 84 | The flow meter on each well. moving_digits / fixed_zeros describe the dial. |
| [`well_readings`](#well_readings) | Wells (groundwater production) | 69,853 | One row per day per well: the meter dial, the chlorine level, who read it. The biggest table. |

## Table details

### Tenancy, users & access

#### `organizations`

The utility company. Nearly every row in the database belongs to one organization.

Rows: 2

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | mediumint(8) | NO | PRI |
| name | varchar(28) | NO |  |
| address | varchar(45) | NO |  |
| city | varchar(60) | NO |  |
| state_id | int(11) | NO | MUL |
| phone | char(14) | NO |  |
| created | datetime | NO |  |
| modified | datetime | NO |  |

Links to: `state_id` → `states.id`

Linked from: `api_credentials.organization_id`, `companies.organization_id`, `elevated_tanks.organization_id`, `groundwater_withdrawal_permits.organization_id`, `lift_stations.organization_id`, `routes.organization_id`, `safe_drinking_water_permits.organization_id`, `sli_ga_addresses.organization_id`, `sli_ga_photos.organization_id`, `sli_ga_service_lines.organization_id`, `sli_locations.organization_id`, `systems.organization_id`, `treatment_plants.organization_id`, `users.organization_id`, `wells.organization_id`

#### `states`

US state lookup used by organizations.state_id (currently empty).

Rows: 1

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| abbr | char(2) | NO |  |
| name | varchar(40) | NO |  |
| created | datetime | YES |  |
| modified | datetime | YES |  |

Linked from: `organizations.state_id`

#### `companies`

Sub-companies within an organization; used by sli_ga_addresses.company_id.

Rows: 6

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| name | varchar(60) | NO |  |
| organization_id | mediumint(8) | NO | MUL |
| created | datetime | NO |  |
| modified | datetime | NO |  |

Links to: `organization_id` → `organizations.id`

Linked from: `sli_ga_addresses.company_id`

#### `users`

The people who log in: operators (web), technicians (phone app), and API users. Roles are yes/no columns.

Rows: 27

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | mediumint(8) | NO | PRI |
| organization_id | mediumint(8) | NO | MUL |
| phone | char(12) | YES | UNI |
| pin_hash | char(60) | YES |  |
| hash_created | datetime | YES |  |
| email | varchar(255) | YES | UNI |
| email_verified | tinyint(1) | YES |  |
| master | tinyint(1) | NO |  |
| operator | tinyint(1) | NO |  |
| operator_permissions | longtext | YES |  |
| technician | tinyint(1) | NO |  |
| technician_permissions | longtext | YES |  |
| debug | tinyint(1) | NO |  |
| api | tinyint(1) | NO |  |
| operator_class | varchar(1) | YES |  |
| first_name | varchar(20) | NO |  |
| last_name | varchar(20) | NO |  |
| created | datetime | NO |  |
| modified | datetime | NO |  |

Links to: `organization_id` → `organizations.id`

Linked from: `api_credentials.user_id`, `lift_station_dials.created_by`, `lift_station_dials.modified_by`, `route_access_revocations.user_id`, `sli_ga_photos.user_id`, `station_readings.user_id`, `users_routes.user_id`, `users_software_meta.user_id`, `verify_email.user_id`, `well_meters.created_by`, `well_meters.modified_by`, `well_readings.user_id`

#### `users_routes`

Which routes each user is allowed to work (one row per user/route pair).

Rows: 104

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | mediumint(8) | NO | PRI |
| user_id | mediumint(8) | NO | MUL |
| route_id | mediumint(8) | NO | MUL |
| created | datetime | NO |  |

Links to: `route_id` → `routes.id`, `user_id` → `users.id`

#### `route_access_revocations`

A record of route access being taken away from a user.

Rows: 0

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| user_id | mediumint(8) | NO | MUL |
| route_id | mediumint(8) | NO | MUL |
| revoked_at | datetime | NO |  |

Links to: `route_id` → `routes.id`, `user_id` → `users.id`

#### `users_software_meta`

Which app version, phone and OS each user has.

Rows: 17

| Column | Type | Can be empty | Key |
|---|---|---|---|
| user_id | mediumint(8) | NO | PRI |
| mobile_os | varchar(150) | NO |  |
| technician_version | varchar(150) | YES |  |
| operator_version | varchar(150) | YES |  |
| phone_model | varchar(150) | YES |  |

Links to: `user_id` → `users.id`

#### `api_credentials`

API key and secret for computer-to-computer access.

Rows: 1

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| api_key | char(32) | NO |  |
| api_secret | char(60) | NO |  |
| organization_id | mediumint(8) | YES | UNI |
| user_id | mediumint(8) | YES | MUL |
| last_queried | bigint(20) | YES |  |

Links to: `organization_id` → `organizations.id`, `user_id` → `users.id`

#### `verify_email`

One-time codes for verifying an email address.

Rows: 11

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| hash | char(10) | NO | UNI |
| user_id | mediumint(8) | NO | MUL |
| created | datetime | NO |  |
| used | tinyint(1) | NO |  |

Links to: `user_id` → `users.id`

#### `verify_phone`

One-time codes for verifying a phone number (empty).

Rows: 0

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| phone | char(12) | NO | UNI |
| pin_hash | char(60) | NO |  |
| hash_created | datetime | NO |  |

#### `verified_numbers`

Phone numbers that passed verification (empty).

Rows: 1

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| phone | char(12) | NO |  |

### Systems, routes & geography

#### `systems`

A water system, usually one subdivision, with its own drinking water permit.

Rows: 30

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | mediumint(8) | NO | PRI |
| name | varchar(45) | NO | MUL |
| organization_id | mediumint(8) | NO | MUL |
| safe_drinking_water_permit_id | int(11) | YES | UNI |
| created | datetime | NO |  |
| modified | datetime | NO |  |

Links to: `organization_id` → `organizations.id`, `safe_drinking_water_permit_id` → `safe_drinking_water_permits.id`

Linked from: `groundwater_withdrawal_permits.system_id`, `lift_stations.system_id`, `sli_ga_addresses.system_id`, `sli_locations.system_id`, `wells.system_id`

#### `routes`

A driving route a technician covers. Wells, lift stations and addresses each belong to a route.

Rows: 8

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | mediumint(8) | NO | PRI |
| name | varchar(21) | NO | MUL |
| organization_id | mediumint(8) | NO | MUL |
| created | datetime | NO |  |
| modified | datetime | NO |  |

Links to: `organization_id` → `organizations.id`

Linked from: `lift_stations.route_id`, `route_access_revocations.route_id`, `sli_ga_addresses.route_id`, `sli_ga_neighborhoods.route_id`, `sli_locations.route_id`, `users_routes.route_id`, `wells.route_id`

#### `ga_counties`

Georgia counties with their FIPS codes (reference data).

Rows: 159

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| fips_code | char(3) | YES |  |
| gww_code | char(3) | YES |  |
| county | varchar(60) | YES |  |
| created | datetime | YES |  |
| modified | datetime | YES |  |

#### `aquifers`

Named aquifers, referenced by groundwater withdrawal permits.

Rows: 31

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | mediumint(8) | NO | PRI |
| name | varchar(80) | YES |  |
| created | datetime | YES |  |
| modified | datetime | YES |  |

Linked from: `groundwater_withdrawal_permits.aquifer_id`

#### `treatment_plants`

Water treatment plants.

Rows: 2

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| name | varchar(60) | NO |  |
| latitude | decimal(17,15) | YES |  |
| longitude | decimal(18,15) | YES |  |
| organization_id | mediumint(8) | NO | MUL |

Links to: `organization_id` → `organizations.id`

#### `elevated_tanks`

Elevated storage tanks (empty).

Rows: 1

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| name | varchar(60) | NO |  |
| latitude | decimal(17,15) | YES |  |
| longitude | decimal(18,15) | YES |  |
| organization_id | mediumint(8) | NO | MUL |

Links to: `organization_id` → `organizations.id`

### Permits

#### `safe_drinking_water_permits`

Safe Drinking Water Act permit numbers; each system links to one.

Rows: 45

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| organization_id | mediumint(8) | NO | MUL |
| permit_number | varchar(45) | NO | MUL |
| created | datetime | NO |  |
| modified | datetime | NO |  |

Links to: `organization_id` → `organizations.id`

Linked from: `systems.safe_drinking_water_permit_id`

#### `groundwater_withdrawal_permits`

Permits to pump groundwater; links an organization, a system and an aquifer.

Rows: 10

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| organization_id | mediumint(8) | NO | MUL |
| system_id | mediumint(8) | NO | MUL |
| aquifer_id | mediumint(8) | NO | MUL |
| permit_number | varchar(8) | NO | MUL |
| permit_holder | varchar(40) | NO |  |
| created | datetime | YES |  |
| modified | datetime | YES |  |

Links to: `aquifer_id` → `aquifers.id`, `organization_id` → `organizations.id`, `system_id` → `systems.id`

Linked from: `wells.groundwater_withdrawal_permit_id`

### Wells (groundwater production)

#### `wells`

The wells, with GPS coordinates, route, system, and permit.

Rows: 50

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | mediumint(8) | NO | PRI |
| name | varchar(45) | NO | MUL |
| latitude | decimal(17,15) | YES |  |
| longitude | decimal(18,15) | YES |  |
| route_id | mediumint(8) | NO | MUL |
| organization_id | mediumint(8) | NO | MUL |
| system_id | mediumint(8) | NO | MUL |
| created | datetime | NO |  |
| modified | datetime | NO |  |
| groundwater_withdrawal_permit_id | int(11) | YES | MUL |
| source_number | varchar(9) | NO |  |
| plant_number | char(3) | NO |  |

Links to: `groundwater_withdrawal_permit_id` → `groundwater_withdrawal_permits.id`, `organization_id` → `organizations.id`, `route_id` → `routes.id`, `system_id` → `systems.id`

Linked from: `well_meters.well_id`, `well_readings.well_id`

#### `well_meters`

The flow meter on each well. moving_digits / fixed_zeros describe the dial.

Rows: 84

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | mediumint(8) | NO | PRI |
| well_id | mediumint(8) | NO | MUL |
| moving_digits | int(11) | NO |  |
| fixed_zeros | int(11) | NO |  |
| active | tinyint(1) | NO |  |
| created | datetime | NO |  |
| modified | datetime | NO |  |
| installation_date | date | NO |  |
| initial_reading | int(11) | NO |  |
| created_by | mediumint(8) | NO | MUL |
| modified_by | mediumint(8) | NO | MUL |

Links to: `created_by` → `users.id`, `modified_by` → `users.id`, `well_id` → `wells.id`

Linked from: `well_readings.meter_id`

#### `well_readings`

One row per day per well: the meter dial, the chlorine level, who read it. The biggest table.

Rows: 69,853

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | mediumint(8) | NO | PRI |
| well_id | mediumint(8) | NO | MUL |
| meter_reading | int(11) | NO |  |
| chlorine_residual | decimal(2,1) | YES |  |
| date_of_reading | date | NO |  |
| user_id | mediumint(8) | YES | MUL |
| comment | varchar(150) | YES |  |
| created | datetime | NO |  |
| modified | datetime | NO |  |
| meter_id | mediumint(8) | NO | MUL |

Links to: `meter_id` → `well_meters.id`, `user_id` → `users.id`, `well_id` → `wells.id`

### Lift stations (wastewater)

#### `lift_stations`

Wastewater pumping stations, with GPS coordinates, route and system.

Rows: 50

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | mediumint(8) | NO | PRI |
| name | varchar(45) | NO | MUL |
| latitude | decimal(17,15) | YES |  |
| longitude | decimal(18,15) | YES |  |
| route_id | mediumint(8) | NO | MUL |
| system_id | mediumint(8) | NO | MUL |
| organization_id | mediumint(8) | NO | MUL |
| created | datetime | NO |  |
| modified | datetime | NO |  |

Links to: `organization_id` → `organizations.id`, `route_id` → `routes.id`, `system_id` → `systems.id`

Linked from: `lift_station_dials.lift_station_id`, `station_readings.lift_station_id`

#### `lift_station_dials`

The hour-meter dials on a lift station's pumps (pump 1 and pump 2).

Rows: 50

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | mediumint(8) | NO | PRI |
| lift_station_id | mediumint(8) | NO | MUL |
| pump | tinyint(1) | NO |  |
| digits_left_of_decimal | int(11) | NO |  |
| digits_right_of_decimal | int(11) | NO |  |
| active | tinyint(1) | NO |  |
| installation_date | date | NO |  |
| initial_reading | decimal(11,2) | NO |  |
| created | datetime | NO |  |
| modified | datetime | NO |  |
| created_by | mediumint(8) | NO | MUL |
| modified_by | mediumint(8) | NO | MUL |

Links to: `created_by` → `users.id`, `lift_station_id` → `lift_stations.id`, `modified_by` → `users.id`

Linked from: `station_readings.lift_station_dial_1_id`, `station_readings.lift_station_dial_2_id`

#### `station_readings`

One row per day per station: both pump dials plus rainfall. Second biggest table.

Rows: 62,101

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | mediumint(8) | NO | PRI |
| lift_station_id | mediumint(8) | NO | MUL |
| lift_station_dial_1_id | mediumint(8) | YES | MUL |
| lift_station_dial_2_id | mediumint(8) | YES | MUL |
| pump1 | decimal(11,2) | YES |  |
| pump2 | decimal(11,2) | YES |  |
| rainfall | decimal(5,2) | NO |  |
| date_of_reading | date | NO |  |
| user_id | mediumint(8) | YES | MUL |
| comment | varchar(150) | YES |  |
| created | datetime | NO |  |
| modified | datetime | NO |  |

Links to: `lift_station_dial_1_id` → `lift_station_dials.id`, `lift_station_dial_2_id` → `lift_station_dials.id`, `lift_station_id` → `lift_stations.id`, `user_id` → `users.id`

### Customer meters

#### `customer_meters`

Customer water meters, keyed by harmony_meter_id / serial_number (from billing).

Rows: 7,954

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| harmony_meter_id | varchar(50) | NO | UNI |
| serial_number | varchar(50) | YES | UNI |

Linked from: `meters_sli_ga_addresses.meter_id`, `sli_ga_addresses.meter_id`

#### `meters_sli_ga_addresses`

Which customer meter is at which inventory address.

Rows: 655

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| meter_id | int(11) | NO | MUL |
| address_id | int(11) | NO | MUL |

Links to: `address_id` → `sli_ga_addresses.id`, `meter_id` → `customer_meters.id`

### Service Line Inventory - Georgia (sli_ga_*)

#### `sli_ga_addresses`

Every customer address in the Georgia lead service line inventory.

Rows: 16,954

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| meter_id | int(11) | YES | MUL |
| harmony_location_id | varchar(60) | YES |  |
| munibilling_id | longtext | YES |  |
| route_number | varchar(6) | YES |  |
| sli_ga_addresses_address_meta_id | int(11) | YES | MUL |
| subdivision_id | int(11) | YES | MUL |
| neighborhood_id | int(11) | YES | MUL |
| organization_id | mediumint(8) | NO | MUL |
| street_address_1 | varchar(199) | NO | MUL |
| street_address_2 | varchar(99) | YES |  |
| city | varchar(99) | NO |  |
| state | char(2) | NO |  |
| zip | char(5) | NO |  |
| construction_year | year(4) | YES |  |
| latitude | decimal(10,8) | YES |  |
| longitude | decimal(11,8) | YES |  |
| other_location_identifier | varchar(200) | YES |  |
| system_id | mediumint(8) | NO | MUL |
| company_id | int(11) | YES | MUL |
| route_id | mediumint(8) | NO | MUL |
| 120water_location_id | int(11) | YES |  |
| created | datetime | NO |  |
| modified | datetime | NO |  |

Links to: `company_id` → `companies.id`, `meter_id` → `customer_meters.id`, `neighborhood_id` → `sli_ga_neighborhoods.id`, `organization_id` → `organizations.id`, `route_id` → `routes.id`, `sli_ga_addresses_address_meta_id` → `sli_ga_addresses.id`, `subdivision_id` → `sli_ga_subdivisions.id`, `system_id` → `systems.id`

Linked from: `meters_sli_ga_addresses.address_id`, `sli_ga_addresses.sli_ga_addresses_address_meta_id`, `sli_ga_service_lines.sli_ga_address_id`

#### `sli_ga_addresses_meta`

Property type / land use for an address.

Rows: 29

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| property_type | varchar(200) | YES |  |
| land_use | varchar(200) | YES |  |
| created | datetime | YES |  |
| modified | datetime | YES |  |

#### `sli_ga_neighborhoods`

Neighborhood names within a route.

Rows: 118

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| name | varchar(60) | NO | MUL |
| system_id | mediumint(8) | YES |  |
| route_id | mediumint(8) | NO | MUL |
| created | datetime | YES |  |
| modified | datetime | YES |  |

Links to: `route_id` → `routes.id`

Linked from: `sli_ga_addresses.neighborhood_id`

#### `sli_ga_subdivisions`

Subdivision names.

Rows: 1,312

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| subdivision | varchar(200) | YES |  |

Linked from: `sli_ga_addresses.subdivision_id`

#### `sli_ga_service_lines`

One row per service line at an address: materials, how they were determined, and the overall lead verdict. Most *_id columns point at a *_responses table.

Rows: 16,926

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| service_line_ownership_type_id | int(11) | YES | MUL |
| system_owned_material_id | int(11) | YES | MUL |
| system_owned_specific_material_id | int(11) | YES | MUL |
| system_owned_material_additional_information | varchar(500) | YES |  |
| system_owned_basis_id | int(11) | YES | MUL |
| system_owned_basis_additional_notes | varchar(500) | YES |  |
| system_owned_installation_date_id | int(11) | YES | MUL |
| system_owned_exact_installation_date | date | YES |  |
| presence_of_lead_connector_id | int(11) | YES | MUL |
| customer_owned_material_id | int(11) | YES | MUL |
| customer_owned_specific_material_id | int(11) | YES | MUL |
| customer_owned_material_additional_information | varchar(500) | YES |  |
| customer_owned_basis_id | int(11) | YES | MUL |
| customer_owned_basis_additional_notes | varchar(500) | YES |  |
| customer_owned_installation_date_id | int(11) | YES | MUL |
| customer_owned_exact_installation_date | date | YES |  |
| overall_service_line_classification_id | int(11) | YES | MUL |
| building_type_id | int(11) | YES | MUL |
| school_or_childcare_id | int(11) | YES | MUL |
| 120water_asset_id | int(11) | YES | UNI |
| sli_ga_address_id | int(11) | NO | MUL |
| organization_id | mediumint(8) | YES | MUL |
| created | datetime | YES |  |
| modified | datetime | YES |  |

Links to: `building_type_id` → `sli_ga_building_type_responses.id`, `customer_owned_basis_id` → `sli_ga_basis_of_classification_responses.id`, `customer_owned_installation_date_id` → `sli_ga_service_line_installation_date_responses.id`, `customer_owned_material_id` → `sli_ga_customer_owned_material_responses.id`, `customer_owned_specific_material_id` → `sli_ga_specific_service_line_material_responses.id`, `organization_id` → `organizations.id`, `overall_service_line_classification_id` → `sli_ga_overall_service_line_classification_responses.id`, `presence_of_lead_connector_id` → `sli_ga_presence_of_lead_connector_responses.id`, `school_or_childcare_id` → `sli_ga_school_or_childcare_facility_responses.id`, `service_line_ownership_type_id` → `sli_ga_service_line_ownership_type_responses.id`, `sli_ga_address_id` → `sli_ga_addresses.id`, `system_owned_basis_id` → `sli_ga_basis_of_classification_responses.id`, `system_owned_installation_date_id` → `sli_ga_service_line_installation_date_responses.id`, `system_owned_material_id` → `sli_ga_system_owned_material_responses.id`, `system_owned_specific_material_id` → `sli_ga_specific_service_line_material_responses.id`

Linked from: `sli_ga_photos.service_line_id`

#### `sli_ga_photos`

Photos of service lines uploaded to S3, with GPS.

Rows: 8

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| photo_uuid | char(36) | NO | UNI |
| service_line_id | int(11) | NO | MUL |
| organization_id | mediumint(8) | NO | MUL |
| user_id | mediumint(8) | NO | MUL |
| side | enum('SYSTEM','CUSTOMER') | NO |  |
| sequence_num | tinyint(4) | NO |  |
| s3_key | varchar(512) | NO |  |
| status | enum('PENDING','UPLOADED','FAILED') | NO | MUL |
| etag | varchar(64) | YES |  |
| content_length | int(11) | YES |  |
| captured_at | datetime | NO |  |
| lat | decimal(10,7) | YES |  |
| lng | decimal(10,7) | YES |  |
| created | datetime | NO |  |
| uploaded_at | datetime | YES |  |

Links to: `organization_id` → `organizations.id`, `service_line_id` → `sli_ga_service_lines.id`, `user_id` → `users.id`

#### `sli_ga_basis_of_classification_responses`

Multiple-choice answers: how a material was determined.

Rows: 9

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| response | varchar(46) | NO |  |
| created | datetime | YES |  |
| modified | datetime | YES |  |

Linked from: `sli_ga_service_lines.customer_owned_basis_id`, `sli_ga_service_lines.system_owned_basis_id`

#### `sli_ga_building_type_responses`

Multiple-choice answers: building type.

Rows: 5

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| response | varchar(38) | YES |  |
| created | datetime | YES |  |
| modified | datetime | YES |  |

Linked from: `sli_ga_service_lines.building_type_id`

#### `sli_ga_customer_owned_material_responses`

Multiple-choice answers: customer-side material category.

Rows: 6

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| response | varchar(54) | NO |  |
| created | datetime | YES |  |
| modified | datetime | YES |  |

Linked from: `sli_ga_service_lines.customer_owned_material_id`

#### `sli_ga_overall_service_line_classification_responses`

Multiple-choice answers: Lead / Non-Lead / GRR / GNRR / Unknown.

Rows: 5

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| response | varchar(55) | NO |  |
| created | datetime | YES |  |
| modified | datetime | YES |  |

Linked from: `sli_ga_service_lines.overall_service_line_classification_id`

#### `sli_ga_presence_of_lead_connector_responses`

Multiple-choice answers: lead connector present?

Rows: 3

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| response | varchar(7) | YES |  |
| created | datetime | YES |  |
| modified | datetime | YES |  |

Linked from: `sli_ga_service_lines.presence_of_lead_connector_id`

#### `sli_ga_school_or_childcare_facility_responses`

Multiple-choice answers: school or childcare?

Rows: 4

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| response | varchar(23) | NO |  |
| created | datetime | YES |  |
| modified | datetime | YES |  |

Linked from: `sli_ga_service_lines.school_or_childcare_id`

#### `sli_ga_service_line_installation_date_responses`

Multiple-choice answers: when it was installed.

Rows: 3

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| response | varchar(9) | NO |  |
| modified | datetime | YES |  |
| created | datetime | YES |  |

Linked from: `sli_ga_service_lines.customer_owned_installation_date_id`, `sli_ga_service_lines.system_owned_installation_date_id`

#### `sli_ga_service_line_ownership_type_responses`

Multiple-choice answers: who owns the line.

Rows: 4

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| response | varchar(18) | YES |  |
| created | datetime | YES |  |
| modified | datetime | YES |  |

Linked from: `sli_ga_service_lines.service_line_ownership_type_id`

#### `sli_ga_specific_service_line_material_responses`

Multiple-choice answers: the exact material (Copper, PVC, ...).

Rows: 14

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| response | varchar(12) | NO |  |
| created | datetime | YES |  |
| modified | datetime | YES |  |

Linked from: `sli_ga_service_lines.customer_owned_specific_material_id`, `sli_ga_service_lines.system_owned_specific_material_id`

#### `sli_ga_system_owned_material_responses`

Multiple-choice answers: system-side material category.

Rows: 6

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| response | varchar(54) | YES |  |
| created | datetime | YES |  |
| modified | datetime | YES |  |

Linked from: `sli_ga_service_lines.system_owned_material_id`

### Service Line Inventory - generic (sli_*)

#### `sli_locations`

Older inventory location records.

Rows: 7,856

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| organization_id | mediumint(8) | NO | MUL |
| system_id | mediumint(8) | NO | MUL |
| 120water_location_id | int(11) | YES |  |
| customer_id | int(11) | YES |  |
| address_line_1 | varchar(99) | NO |  |
| address_line_2 | varchar(99) | YES |  |
| city | varchar(59) | NO |  |
| state | char(2) | NO |  |
| zip | char(5) | NO |  |
| county | varchar(99) | YES |  |
| mailing_address_line_1 | varchar(99) | YES |  |
| mailing_address_line_2 | varchar(99) | YES |  |
| mailing_city | varchar(59) | YES |  |
| mailing_state | char(2) | YES |  |
| mailing_zip | char(5) | YES |  |
| building | varchar(99) | YES |  |
| neighborhood_id | int(11) | YES | MUL |
| location_name | varchar(99) | YES |  |
| route_id | mediumint(8) | NO | MUL |
| latitude | decimal(10,8) | NO |  |
| longitude | decimal(11,8) | NO |  |
| gis_location_id | varchar(99) | YES |  |
| dwelr_code | varchar(99) | YES |  |
| lcr_tier_id | int(11) | YES | MUL |
| property_classification_id | int(11) | YES | MUL |
| parcel_number | varchar(99) | YES |  |
| year_built | char(4) | YES |  |
| lot_square_feet | decimal(10,2) | YES |  |
| water_main_id | int(11) | YES | MUL |
| curb_stop_id | int(11) | YES | MUL |
| meter_id | int(11) | YES |  |
| other_buildings_on_property | tinyint(1) | YES |  |
| has_children_under_7 | tinyint(1) | YES |  |
| has_pregnant_women | tinyint(1) | YES |  |
| disadvantaged_neighborhood | tinyint(1) | YES |  |
| property_owned_by_business | tinyint(1) | YES |  |
| business_name | varchar(99) | YES |  |
| estimated_home_value | decimal(12,2) | YES |  |
| notes | varchar(99) | YES |  |
| point_of_entry_id | int(11) | YES | MUL |
| building_plumbing_lead_solder_id | int(11) | YES | MUL |
| lcr_sampling_site_id | int(11) | YES | MUL |
| sensitive_population_id | int(11) | YES | MUL |

Links to: `building_plumbing_lead_solder_id` → `sli_building_plumbing_lead_solder_responses.id`, `curb_stop_id` → `sli_curb_stops.id`, `lcr_sampling_site_id` → `sli_lcr_sampling_site_responses.id`, `lcr_tier_id` → `sli_lcr_tier_responses.id`, `neighborhood_id` → `sli_neighborhoods.id`, `organization_id` → `organizations.id`, `point_of_entry_id` → `sli_point_of_entry_responses.id`, `property_classification_id` → `sli_property_classification_responses.id`, `route_id` → `routes.id`, `sensitive_population_id` → `sli_sensitive_population_responses.id`, `system_id` → `systems.id`, `water_main_id` → `sli_water_mains.id`

#### `sli_neighborhoods`

Neighborhood lookup for sli_locations.

Rows: 36

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| name | varchar(99) | NO |  |
| route_id | mediumint(8) | NO |  |
| organization_id | mediumint(8) | NO |  |
| created | datetime | NO |  |
| modified | datetime | NO |  |

Linked from: `sli_locations.neighborhood_id`

#### `sli_service_lines`

Older service line records (empty).

Rows: 0

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| 120water_location_id | int(11) | YES |  |
| locations_id | int(11) | YES |  |
| 120water_asset_id | int(11) | YES |  |
| description | varchar(150) | YES |  |
| status_id | int(11) | YES |  |
| customer_owned_material_id | int(11) | YES |  |
| customer_owned_lead_solder | int(11) | YES |  |
| customer_owned_user_id | int(11) | YES |  |
| customer_owned_verified_date | date | YES |  |
| customer_owned_verification_method_id | int(11) | YES |  |
| customer_owned_removal_date | date | YES |  |
| customer_owned_installed_date | date | YES |  |
| customer_owned_line_depth | int(11) | YES |  |
| customer_owned_line_diameter_id | int(11) | YES |  |
| system_owned_material_id | int(11) | YES |  |
| system_owned_lead_solder_id | int(11) | YES |  |
| system_owned_verified_by_id | int(11) | YES |  |
| system_owned_verified_date | date | YES |  |
| system_owned_verification_method_id | int(11) | YES |  |
| system_owned_removal_date | date | YES |  |
| system_owned_installed_date | date | YES |  |
| system_owned_line_depth | int(11) | YES |  |
| system_owned_line_diameter_id | int(11) | YES |  |
| lead_fittings_id | int(11) | YES |  |
| fitting_verified_by_id | int(11) | YES |  |
| fittings_verified_date | date | YES |  |
| fittings_verification_method_id | int(11) | YES |  |
| latitude | decimal(10,8) | YES |  |
| longitude | decimal(11,8) | YES |  |
| system_owned_classification_basis_id | int(11) | YES |  |
| customer_owned_classification_basis_id | int(11) | YES |  |
| system_owned_notes | varchar(150) | YES |  |
| customer_owned_notes | varchar(150) | YES |  |
| system_owned_previously_lead_id | int(11) | YES |  |
| lead_solder_id | int(11) | YES |  |
| other_lead_equipment | varchar(100) | YES |  |
| customer_owned_verified | tinyint(1) | YES |  |
| system_owned_verified | tinyint(1) | YES |  |
| system_owned_material_other | varchar(100) | YES |  |
| system_owned_verification_method_other | varchar(100) | YES |  |
| customer_owned_material_other | varchar(100) | YES |  |
| customer_owned_verification_method_other | varchar(100) | YES |  |
| fittings_verification_method_other | varchar(100) | YES |  |
| system_owned_installed_after_lead_ban_id | int(11) | YES |  |
| customer_owned_installed_after_lead_ban | int(11) | YES |  |
| ownership_id | int(11) | YES |  |
| system_owned_diameter_over_two_inches | tinyint(1) | YES |  |
| customer_owned_diameter_over_two_inches | tinyint(1) | YES |  |
| consumer_notice_completed | tinyint(1) | YES |  |
| consumer_notice_completion_date | date | YES |  |
| customer_owned_classification_basis_notes | varchar(100) | YES |  |
| system_owned_classification_basis_notes | varchar(100) | YES |  |

#### `sli_curb_stops`

Curb stop records (empty).

Rows: 0

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| name | varchar(99) | NO |  |
| user_id | mediumint(8) | NO |  |
| service_line_diameter_id | int(11) | NO |  |
| curb_stop_installed_year | year(4) | YES |  |

Linked from: `sli_locations.curb_stop_id`

#### `sli_water_mains`

Water main records (empty).

Rows: 0

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| name | varchar(99) | NO |  |
| water_main_material_id | int(11) | NO |  |
| water_main_size | decimal(5,2) | NO |  |
| water_main_installed_year | char(4) | YES |  |
| created | datetime | NO |  |
| modified | datetime | NO |  |
| neighborhood_id | int(11) | NO |  |
| water_main_removal_year | char(4) | YES |  |

Linked from: `sli_locations.water_main_id`

#### `sli_service_line_diameter`

Multiple-choice answers: pipe diameter.

Rows: 18

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| display_value | varchar(10) | NO |  |
| decimal_value | decimal(7,5) | NO |  |
| raw_value | varchar(10) | NO |  |

#### `sli_water_main_materials`

Multiple-choice answers: water main material.

Rows: 27

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| material | varchar(19) | NO |  |

#### `sli_building_plumbing_lead_solder_responses`

Multiple-choice answers: lead solder in the building?

Rows: 3

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| value | varchar(7) | NO |  |

Linked from: `sli_locations.building_plumbing_lead_solder_id`

#### `sli_curb_stop_materials_responses`

Multiple-choice answers: curb stop material.

Rows: 17

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| name | varchar(10) | NO |  |

#### `sli_customer_owned_classification_basis_responses`

Multiple-choice answers: basis for customer-side classification.

Rows: 23

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| response | varchar(70) | YES |  |

#### `sli_fittings_verification_method_responses`

Multiple-choice answers: how fittings were checked.

Rows: 19

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| response | varchar(38) | NO |  |

#### `sli_installed_after_lead_ban_responses`

Multiple-choice answers: installed after the lead ban?

Rows: 3

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| response | varchar(7) | NO |  |

#### `sli_lcr_sampling_site_responses`

Multiple-choice answers: Lead & Copper Rule sampling site?

Rows: 3

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| value | varchar(7) | NO |  |

Linked from: `sli_locations.lcr_sampling_site_id`

#### `sli_lcr_tier_responses`

Multiple-choice answers: LCR sampling tier.

Rows: 5

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| tier | char(6) | NO |  |

Linked from: `sli_locations.lcr_tier_id`

#### `sli_point_of_entry_responses`

Multiple-choice answers: point-of-entry treatment.

Rows: 3

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| value | varchar(7) | NO |  |

Linked from: `sli_locations.point_of_entry_id`

#### `sli_property_classification_responses`

Multiple-choice answers: property classification.

Rows: 14

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| classification | varchar(50) | NO |  |

Linked from: `sli_locations.property_classification_id`

#### `sli_sensitive_population_responses`

Multiple-choice answers: sensitive population served?

Rows: 7

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| value | varchar(23) | NO |  |

Linked from: `sli_locations.sensitive_population_id`

#### `sli_service_line_materials_responses`

Multiple-choice answers: service line material.

Rows: 26

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| data_code | varchar(5) | NO |  |
| selection_value | varchar(45) | NO |  |
| raw_value | varchar(17) | NO |  |

#### `sli_system_owned_classification_basis_responses`

Multiple-choice answers: basis for system-side classification.

Rows: 31

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| response | varchar(70) | YES |  |

### Operations & diagnostics

#### `errors`

A log of errors from the phone/web app: what was sent, which page, what went wrong, when.

Rows: 270

| Column | Type | Can be empty | Key |
|---|---|---|---|
| id | int(11) | NO | PRI |
| req_body | longtext | YES |  |
| req_decoded | longtext | YES |  |
| req_route | longtext | YES |  |
| error | text | YES |  |
| occured | datetime | YES |  |
