#!/usr/bin/env bash

PROGNAME=$(basename "$0")

NORMAL="\\033[0;39m"
RED="\\033[1;31m"

usage() {
  echo "USAGE: "
  # echo "If pathdb:"
  printf "    ${RED}$PROGNAME user passwd manifest${NORMAL}\n"
  # echo "Else:"
  # echo "$PROGNAME dbhost dbport dbname manifest"
  exit 1
}

error_exit() {
  echo "${PROGNAME}: ${1:-"Error"}" 1>&2
  exit 1
}

# Check input
if [[ $# -eq 3 ]] ; then
  # do the thing
  python3.7 /app/quip_csv.py --dbhost "ca-mongo" --dbport 27017 --dbname camic --pathdb --url "http://quip-pathdb" "$@" || error_exit $LINENO
else
  usage  
fi

SECONDS=0

ELAPSED="Elapsed: $(($SECONDS / 3600))hrs $(($SECONDS / 60 % 60))min $(($SECONDS % 60))sec"
echo "$ELAPSED"

#==============
# if [[ $# -eq 4 ]] ; then
# python3.7 /app/quip_csv.py --dbhost $1 --dbport $2 --dbname $3 --manifest $4 || error_exit $LINENO
# else
# python3.7 /app/quip_csv.py --dbhost "ca-mongo" --dbport 27017 --dbname camic --pathdb --url "http://quip-pathdb" "$@" || error_exit $LINENO
# fi
