#!/usr/bin/env bash

PROGNAME=$(basename "$0")

usage() {
  echo "Usage: $PROGNAME --dbhost A --dbport B --dbname C --pathdb --url D --user E --passwd F --manifest G"
  exit 1
}

error_exit() {
  echo "${PROGNAME}: ${1:-"Error"}" 1>&2
  exit 1
}

if [[ $# -lt 6 ]] ; then
  usage
fi

SECONDS=0

python3.7 /app/quip_csv.py --dbhost $1 --dbport $2 --dbname $3 --pathdb --url $4 --user $5 --passwd $6 --manifest $7 || error_exit $LINENO

ELAPSED="Elapsed: $(($SECONDS / 3600))hrs $(($SECONDS / 60 % 60))min $(($SECONDS % 60))sec"
echo "$ELAPSED"
