#! /usr/bin/env bash
#
# backupdb.sh
# Copyright (C) 2020 Thomas Butterworth <dmr@davidrosenberg.me>
#
# Usage: backupdb.sh [-vhq] [--target=<TARGETFILE>]
#
# restore the database backup BACKUPFILE to database DBNAME
#
# Options:
#   -h --help
#   -v       verbose mode
#   -q       quiet mode
#   --target=<TARGETFILE>
#

set -o pipefail

unset PROMPT_COMMAND
PS1=" >"

if [ ${DEBUG_SCRIPT:-0} -gt 1 ]; then
  set -x
fi


PG_DUMP="$(which pg_dump)"
GIT_TAG="$(git describe --tags | tail -n1)"
DIRNAME="$(which gdirname || which dirname)"
READLINK="$(which greadlink || which readlink)"
WORKINGDIR="$($READLINK -f $($DIRNAME $0)/..)"
source "$WORKINGDIR/scripts/common.sh"
trap - EXIT
source $WORKINGDIR/scripts/docopts.sh --auto "$@"
version="0.0.1"
helptext="$(docopt_get_help_string $0)"
usage=$(docopt_get_help_string "$0")
eval "$(docopts -A ARGS -V "$VERSION" -h "$usage" : "$@")"


debuglog() {
  [ ${DEBUG_SCRIPT:-0} -gt 0 ] && echo "$@" > /dev/stderr
}

if [[ "${ARGS[-v]}" == true ]]; then
  DEBUG_SCRIPT=${DEBUG_SCRIPT:-1}
  debuglog "Setting DEBUG_SCRIPT=1 since verbose option passed"
fi

usage() {
  echo "$helptext"
}

if [ -a ${ARGS[--target]} ]; then
  TARGET="$($DIRNAME $0)/../backups/signout-${GIT_TAG}.sql.gz"
else
  TARGET=${ARGS[--target]}
fi
debuglog "Target file specified as '$TARGET'"
mkdir -p "$WORKINGDIR/backups" > /dev/null 2>&1
if [ -e "$TARGET" ]; then
  echo "BACKUP FILE $TARGET already exists."
  echo "Use a different targetfile or bump the git tag if using the default backupfile"
  usage
  trap - EXIT
  exit 255
else
  PGPASSWORD=$PASSWD $PG_DUMP -U $USER $DBNAME | gzip - - > ${TARGET}
  if [ $? -gt 0 ]; then
    echo "BACKUP FAILED"
    rm -i "$TARGET"
    exit 3
  else
    echo "Backed up database to file $TARGET"
  fi
fi

trap - EXIT
exit 0

# vim: ft=sh
