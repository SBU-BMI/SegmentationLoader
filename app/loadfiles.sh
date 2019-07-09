#!/usr/bin/env bash

PROGNAME=$(basename "$0")

usage() {
  echo "Usage: "
  echo "If pathdb:"
  echo "$PROGNAME dbhost dbport dbname url user passwd manifest"
  echo "Else:"
  echo "$PROGNAME dbhost dbport dbname manifest"
  exit 1
}

error_exit() {
  echo "${PROGNAME}: ${1:-"Error"}" 1>&2
  exit 1
}

if [[ $# -eq 0 ]] ; then
  echo "No arguments supplied"
  usage
fi

if [[ $# -eq 4 ]] ; then
  python3.7 /app/quip_csv.py --dbhost $1 --dbport $2 --dbname $3 --manifest $4 || error_exit $LINENO
else
  python3.7 /app/quip_csv.py --dbhost $1 --dbport $2 --dbname $3 --pathdb --url $4 --user $5 --passwd $6 --manifest $7 || error_exit $LINENO
fi

SECONDS=0


ELAPSED="Elapsed: $(($SECONDS / 3600))hrs $(($SECONDS / 60 % 60))min $(($SECONDS % 60))sec"
echo "$ELAPSED"
