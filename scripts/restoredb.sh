#! /usr/bin/env bash
# Copyright Thomas M. Butterworth
# Distributed under terms of the MIT license.
#
# Usage: restoredb.sh [-vhq] BACKUPFILE [DBNAME]
#
# restore the database backup BACKUPFILE to database DBNAME
#
# Arguments:
#   DBNAME      Optional database name
#   BACKUPFILE  SQL Backup File
#
# Options:
#   -h --help
#   -v       verbose mode
#   -q       quiet mode
#

set +x
if [ ${DEBUG_SCRIPT:-0} -gt 1 ]; then
  set -x
fi

WHICH="$(which gwhich || which which)"
DIRNAME="$($WHICH gdirname || $WHICH dirname)"
READLINK="$($WHICH greadlink || $WHICH readlink)"
WORKINGDIR="$($READLINK -f $($DIRNAME ${BASH_SOURCE[0]})/..)"
source "$WORKINGDIR/scripts/common.sh"
source "$WORKINGDIR/scripts/docopts.sh" --auto "$@"
version=0.0.1
helptext=$(docopt_get_help_string $0)

debuglog() {
  if [ ${DEBUG_SCRIPT:-0} -gt 1 ]; then
    $ECHO "$@" > /dev/stderr
  fi
}

[ ${DEBUG_SCRIPT:-0} -gt 0 ] && debuglog "WHICH=$WHICH" \
 && debuglog "DIRNAME=$DIRNAME" \
 && debuglog "READLINK=$READLINK" \
 && debuglog "WORKINGDIR=$WORKINGDIR"

usage() {
  printf "$helptext"
}

RESTORECMD="cat ${ARGS[BACKUPFILE]} | gunzip |"

serial=$(date +%s)
newbackup=$($READLINK -f ${ARGS[BACKUPFILE]} | perl -p -e "s/(sql.*)$/$serial.\\1/")
if [ -e "$newbackup" ]; then 
  cleanup "Backup file '$newbackup' already exists!  Aborting" 2
fi

$WORKINGDIR/scripts/backupdb.sh --target="$newbackup"
if [ $? -gt 0 ]; then
  cleanup "Error storing the existing database.  Aborting" 3
fi
debuglog "Backed up to '$newbackup'"

if [ -z "${ARGS[DBNAME]}" ]; then
  targetdb=$DBNAME
else
  targetdb=${ARGS[DBNAME]}
fi


cat<<EOF | $PSQL -U $USER $targetdb >/dev/null 2>&1
DROP TABLE IF EXISTS assignments CASCADE;
DROP TABLE IF EXISTS nightfloat CASCADE;
DROP TABLE IF EXISTS service CASCADE;
DROP TABLE IF EXISTS signout CASCADE;
EOF
debuglog "clearing existing db"

RESTORECMD="$RESTORECMD $PSQL -U $USER $targetdb"
debuglog "executing '$RESTORECMD'"
eval "PGPASSWORD=$PASSWD $RESTORECMD" > /dev/null 2>&1

if [ $? -gt 0 ]; then
  cleanup "Error restoring database.  Aborting" 4
fi
debuglog "Restored '$targetdb'"

rm -f "$TMPFILE" "$LOGFILE"
trap - EXIT

exit 0
