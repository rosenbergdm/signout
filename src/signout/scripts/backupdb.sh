#! /usr/bin/env bash
# -*- coding: utf-8 -*-
# vim:enc=utf-8
#
#    This file is part of signout.py the house staff web-based signout
#    manager for MSKCC.
#    Copyright © 2020-2021 David M. Rosenberg <dmr@davidrosenberg.me>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#
# Usage: backupdb.sh [-vhq] [--target=<TARGETFILE>] [--dbname=<DBNAME>]
#
# backup the database DBNAME to file TARGETFILE
#
# Options:
#   -h --help
#   -v       verbose mode
#   -q       quiet mode
#   --target=<TARGETFILE>
#   --dbname=<DBNAME>
#

set -o pipefail
set +x
if [ ${DEBUG_SCRIPT:-0} -gt 1 ]; then
  set -x
fi
if echo -- "$@" | grep -- ' -v'>/dev/null; then
  if [ ${DEBUG_SCRIPT:-0} -lt 2 ]; then
    DEBUG_SCRIPT=1
  fi
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

if [ -z ${ARGS[--dbname]} ]; then
  DB=$DBNAME
else
  DB=${ARGS[--dbname]}
fi
debuglog "DB=$DB"

if [ -z ${ARGS[--target]} ]; then
  TARGET="$($DIRNAME $0)/../backups/$DB-${GIT_TAG}.sql.gz"
else
  TARGET=${ARGS[--target]}
fi

debuglog "Target file specified as '$TARGET'"
mkdir -p "$WORKINGDIR/backups" > /dev/null 2>&1
if [ -e "$TARGET" ]; then
  echo "BACKUP FILE $TARGET already exists."
  echo "Use a different targetfile or bump the git tag if using the default backupfile"
  trap - EXIT
  exit 255
else
  PGPASSWORD=$PASSWD $PG_DUMP -U $USER $DB | gzip - - > ${TARGET}
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
