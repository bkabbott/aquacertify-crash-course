#!/usr/bin/env bash
# Opens the MariaDB command line, already logged in to our database.
# Type SQL ending with a semicolon, press Enter. Type  exit  to leave.
exec mariadb -u aquacertify -paquacertify aquacertify "$@"
