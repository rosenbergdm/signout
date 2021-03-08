#! /usr/bin/env bash
# Copyright Thomas M. Butterworth
# Distributed under terms of the MIT license.
#
# Usage: restoredb.sh [-vhq] [--debug] [--dbname=<DBNAME>] BACKUPFILE
#
# restore the database backup BACKUPFILE to database DBNAME
#
# Arguments:
#   BACKUPFILE  SQL Backup File
#
# Options:
#   -h --help           display usage
#   -v --verbose        verbose mode
#   -q --quiet          quiet mode
#   --debug             debug this script
#   --dbname=<DBNAME>   Database [default=signout]
#

set +x
set -o pipefail
if [ ${DEBUG_SCRIPT:-0} -gt 1 ]; then
  echo "TODO"
fi
if echo -- "$@" | grep -- ' -v'>/dev/null; then
  echo "-v option passed, setting DEBUG_SCRIPT"
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
[[ ${ARGS[--debug]} == true ]] && docopt_print_ARGS
if [[ "${ARGS[--verbose]}" == true ]]; then
  DEBUG_SCRIPT=${DEBUG_SCRIPT:-1}
fi

if [ -z "${ARGS[--dbname]}" ]; then
  targetdb=$DBNAME
else
  targetdb=${ARGS[--dbname]}
fi


failure() {
  local lineno=$1
  local msg=$2
  echo "****Failed at ${BASH_SOURCE[0]}:$lineno: $msg******"
  echo "ABORTING"
  rm -f "$TMPFILE" "$LOGFILE"
  exit 9
}
trap 'failure ${LINENO} "$BASH_COMMAND"' ERR

[ ${DEBUG_SCRIPT:-0} -gt 0 ] && debuglog "WHICH=$WHICH" \
 && debuglog "DIRNAME=$DIRNAME" \
 && debuglog "READLINK=$READLINK" \
 && debuglog "WORKINGDIR=$WORKINGDIR"


serial=$($DATE +%N | sed -e 's/\(.\{6\}\).*$/\1/')
_newbackup=$($READLINK -f ${ARGS[BACKUPFILE]} | perl -p -e "s/(\.sql(.gz)?$)$/.$serial\\1/")
newbackup="$WORKINGDIR/backups/$($BASENAME $_newbackup  | sed -e "s/signout2\{0,1\}-/$targetdb-/g")"

if [ -f "$newbackup" ]; then 
  $PRINTF "Backup file '$newbackup' already exists!  Aborting\n"
  rm -f "$TMPFILE" "$LOGFILE"
  trap - EXIT
  exit 3
fi

$WORKINGDIR/scripts/backupdb.sh --target="$newbackup" --dbname="$targetdb"
if [ $? -gt 0 ]; then
  $ECHO "Error storing the existing database.  Aborting" 
  rm -f "$TMPFILE" "$LOGFILE"
  trap - EXIT
  exit 2
fi
debuglog "Backed '$targetdb' up to '$newbackup'"



export PGPASSWORD=$PASSWD
$PRINTF "Dropping tables from $targetdb as $USER\n" || echo "MSG FAILED"
read -p "Press enter to continue (THIS IS DESTRUCTIVE)" _z
echo "DROP SCHEMA public CASCADE; CREATE SCHEMA public" | $PSQL -U $USER $targetdb
if [ $? -gt 0 ]; then
  failure ${LINENO} "Failed to drop schema in $targetdb"
else
  $PRINTF "SUCCESS Dropping tables\n\n"
fi

rawsqlfile=${ARGS[BACKUPFILE]//.gz}
rezip=0
if echo ${ARGS[BACKUPFILE]} | egrep '\.gz$' >/dev/null; then
  rezip=1
  gunzip ${ARGS[BACKUPFILE]}
  debuglog "Unzipped backup to '$rawsqlfile'"
fi

debuglog "Executing '$rawsqlfile'... "
cat $rawsqlfile | $PSQL -U $USER $targetdb

if [ $? -gt 0 ]; then
  failure ${LINENO} "FAILED to execute $rawsqlfile on $targetdb"
fi

debuglog "Restored '${ARGS[BACKUPFILE]}' to '$targetdb'"
[ $rezip -gt 0 ] && gzip ${ARGS[BACKUPFILE]//.gz}

rm -f "$TMPFILE" "$LOGFILE"
trap - EXIT
exit 0
