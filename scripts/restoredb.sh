#! /usr/bin/env bash
# Copyright Thomas M. Butterworth
# Distributed under terms of the MIT license.
#
# Usage: restoredb.sh [-hvqV] BACKUPFILE [DBNAME]
#
# restore the database backup BACKUPFILE to database DBNAME
#
# Arguments:
#   BACKUPFILE  SQL Backup File
#   DBNAME      Optional database name
#
# Options:
#   -h --help
#   -v       verbose mode
#   -q       quiet mode
#   -V       Print program version
#

set +x
set -o pipefail
if [ ${DEBUG_SCRIPT:-0} -gt 1 ]; then
  set -v
  # set -x
fi
if echo -- "$@" | grep -- '-v'>/dev/null; then
  if [ ${DEBUG_SCRIPT:-0} -lt 2 ]; then
    DEBUG_SCRIPT=1
  fi
fi

WHICH="$(which gwhich || which which)"
DIRNAME="$($WHICH gdirname || $WHICH dirname)"
READLINK="$($WHICH greadlink || $WHICH readlink)"
WORKINGDIR="$($READLINK -f $($DIRNAME ${BASH_SOURCE[0]})/..)"
source "$WORKINGDIR/scripts/common.sh"
trap - EXIT
source $WORKINGDIR/scripts/docopts.sh --auto "$@"
# VERSION=0.0.1
# helptext=$(docopt_get_help_string $0)
# usage=$(docopt_get_help_string "$0")
# eval "$(docopts -A ARGS -V "$VERSION" -h "$usage" : "$@")"
docopt_print_ARGS


cleanup() {
  errorcode=${2:-255}
  errormessage="$1"
  if [ -z "$errormessage" ]; then
    $PRINTF "An unknown error occured.  Aborting.\n"
    $PRINTF "$helptext\n"
    trap - EXIT
  else 
    $PRINTF "$errormessage\n"
    $PRINTF "Aborting\n" 
    trap - EXIT
  fi
  exit $errorcode
}
trap cleanup EXIT

[ ${DEBUG_SCRIPT:-0} -gt 0 ] && debuglog "WHICH=$WHICH" \
 && debuglog "DIRNAME=$DIRNAME" \
 && debuglog "READLINK=$READLINK" \
 && debuglog "WORKINGDIR=$WORKINGDIR"

RESTORECMD="cat ${ARGS[BACKUPFILE]} | gunzip |"

serial=$(date +%s)
newbackup=$($READLINK -f ${ARGS[BACKUPFILE]} | perl -p -e "s/(sql.*)$/$serial.\\1/")
if [ -e "$newbackup" ]; then 
  cleanup "Backup file '$newbackup' already exists!  Aborting" 2
  exit 2
fi


$WORKINGDIR/scripts/backupdb.sh --target="$newbackup"
if [ $? -gt 0 ]; then
  cleanup "Error storing the existing database.  Aborting" 3
  exit 3
fi
debuglog "Backed up to '$newbackup'"

if [ -z "${ARGS[DBNAME]}" ]; then
  targetdb=$DBNAME
else
  targetdb=${ARGS[DBNAME]}
fi

$PRINTF "Dropping tables from $targetdb as $USER\n"
read -p "Press enter to continue" x
echo " DROP TABLE IF EXISTS assignments CASCADE; \
  DROP TABLE IF EXISTS nightfloat CASCADE; \
  DROP TABLE IF EXISTS service CASCADE; \
  DROP TABLE IF EXISTS signout CASCADE; " | \
  PGPASSWORD=$PASSWD $PSQL -U $USER $targetdb >/dev/null 2>&1
debuglog "clearing existing db"

RESTORECMD="$RESTORECMD $PSQL -U $USER $targetdb"
debuglog "executing '$RESTORECMD'"
export PGPASSWORD=$PASSWD
eval "PGPASSWORD=$PASSWD $RESTORECMD" > /dev/null 2>&1
unset PGPASSWORD

if [ $? -gt 0 ]; then
  cleanup "Error restoring database.  Aborting" 4
fi
debuglog "Restored '$targetdb'"

rm -f "$TMPFILE" "$LOGFILE"
trap - EXIT

exit 0
