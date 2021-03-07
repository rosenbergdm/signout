#! /usr/bin/env bash
#
# backupdb.sh
# Copyright (C) 2020 Thomas Butterworth <dmr@davidrosenberg.me>
#
# Distributed under terms of the MIT license.
#

set -o pipefail

unset PROMPT_COMMAND
PS1=" >"

if [ ${DEBUG_SCRIPT:-0} -gt 1 ]; then
  set -x
fi

debuglog() {
  [ ${DEBUG_SCRIPT:-0} -gt 0 ] && echo "$@" > /dev/stderr
}

usage() {
  echo USAGE:
  echo
  echo -e "\t\t > $0 [--target=TARGETFILE]"
  echo 
  echo "Backs up the datebase.  If targetfile isn't given, uses a name defined from the git tag"
  echo 
}

PG_DUMP="$(which pg_dump)"
GIT_TAG="$(git describe --tags | tail -n1)"
DIRNAME="$(which gdirname || which dirname)"
READLINK="$(which greadlink || which readlink)"
WORKINGDIR="$($READLINK -f $($DIRNAME $0)/..)"
TARGET="$($DIRNAME $0)/../backups/signout-${GIT_TAG}.sql.gz"
if echo -- "$@" | grep "target.*sql.*" > /dev/null; then
  TARGET=$(echo -- "$@" | perl -p -e 's/ /\n/g' | grep -- target | perl -p -e 's/.*target=(.*)$/\1/g')
  debuglog "target file specified as '$TARGET'"
else
  TARGET="$WORKINGDIR/backups/signout-$GIT_TAG.sql.gz"
  debuglog "using default target file '$TARGET'"
fi
if echo -- "$@"  | grep -- "-\{1,2\}h" > /dev/null; then
  debuglog "help requested"
  usage
  exit 1
fi
debuglog "TARGET=$TARGET"
mkdir -p "$WORKINGDIR/backups" > /dev/null 2>&1
PASSWD="$(cat "$WORKINGDIR/dbsettings.json" | grep pass | sed -e 's#"##g' | awk '{print $2}')"
USER="$(cat $WORKINGDIR/dbsettings.json | grep username | sed -e 's#["|,]##g' | awk '{print $2}')"
DBNAME="$(cat $WORKINGDIR/dbsettings.json | grep dbname | sed -e 's#["|,]##g' | awk '{print $2}')"
if [ -f "$TARGET" ]; then
  echo "BACKUP FILE $TARGET already exists. Use a different targetfile or bump the git tag if using the default backupfile"
  echo
  usage
  echo
  exit 255
else
  PGPASSWORD="$PASSWD" $PG_DUMP "$DBNAME" -U "$USER" | gzip - - > "${TARGET}"
  if [ $? -gt 0 ]; then
    echo "BACKUP FAILED"
    rm -i "$TARGET"
    exit 3
  else
    echo "Backed up database to file $TARGET"
  fi
fi

set +x
exit 0


# vim: ft=sh
