#!/usr/bin/env bash

PROGNAME=$(basename "$0")

usage() {
	echo "Usage: $PROGNAME pathdb-url collection study subject user password"
	exit 1
}

error_exit() {
  echo "${PROGNAME}: ${1:-"Error"}" 1>&2
  echo "Line $2"
  exit 1
}

if [[ $# -lt 6 ]] ; then
	usage
fi

SECONDS=0
for directory in $(find ./tmp/* -type d);
do
  echo "$directory"
  python3.7 /app/quip_csv.py --dbhost ca-mongo --dbport 27017 --dbname camic --quip "$directory" --pathdb --url "$1" --collection "$2" --study "$3" --subject "$4" --user "$5" --passwd "$6" || error_exit $LINENO
done

ELAPSED="Elapsed: $(($SECONDS / 3600))hrs $(($SECONDS / 60 % 60))min $(($SECONDS % 60))sec"
echo "$ELAPSED"
