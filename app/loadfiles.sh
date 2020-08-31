#!/usr/bin/env bash

PROGNAME=$(basename "$0")

usage() {
  echo "Usage: "
  # echo "If pathdb:"
  echo "$PROGNAME user passwd manifest"
  # echo "Else:"
  # echo "$PROGNAME dbhost dbport dbname manifest"
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

SECONDS=0

# if [[ $# -eq 4 ]] ; then
# python3.7 /app/quip_csv.py --dbhost $1 --dbport $2 --dbname $3 --manifest $4 || error_exit $LINENO
# else
python3.7 /app/quip_csv.py --dbhost "ca-mongo" --dbport 27017 --dbname camic --pathdb --url "http://quip-pathdb:8080" "$@" || error_exit $LINENO
# fi

ELAPSED="Elapsed: $(($SECONDS / 3600))hrs $(($SECONDS / 60 % 60))min $(($SECONDS % 60))sec"
echo "$ELAPSED"
