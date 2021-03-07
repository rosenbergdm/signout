#! /usr/bin/env bash
#
# common.sh
# Copyright (C) 2020 Thomas Butterworth <dmr@davidrosenberg.me>
#
# Distributed under terms of the MIT license.
#

set -o pipefail

set +x
if [ ${DEBUG_SCRIPT:-0} -gt 1 ]; then
  set -x
fi

ECHO="$($WHICH gecho || $WHICH echo)"
PRINTF="$($WHICH gprintf || $WHICH printf)"
debuglog() {
  if [ ${DEBUG_SCRIPT:-0} -gt 0 ]; then
    $ECHO "$@" > /dev/stderr
  fi
}
WHICH="$(which gwhich || which which)" && debuglog "WHICH=$WHICH"
DIRNAME="$($WHICH gdirname || $WHICH dirname)" && debuglog "DIRNAME=$DIRNAME"
READLINK="$($WHICH greadlink || $WHICH readlink)" && debuglog "READLINK=$READLINK"
WORKINGDIR="$($READLINK -f $($DIRNAME ${BASH_SOURCE[0]})/..)" && debuglog "WORKINGDIR=$WORKINGDIR"
JQ=$($WHICH jq)
if [ -z "$JQ" ]; then
  debuglog "not using jq"
  PASSWD="$(cat "$WORKINGDIR/dbsettings.json" | grep DBPASSWORD | sed -e 's#"##g' | awk '{print $2}')" && debuglog "PASSWD=****"
  USER="$(cat $WORKINGDIR/dbsettings.json | grep DBUSER | sed -e 's#["|,]##g' | awk '{print $2}')" && debuglog "USER=$USER"
  DBNAME="$(cat $WORKINGDIR/dbsettings.json | grep DBNAME | sed -e 's#["|,]##g' | awk '{print $2}')" && debuglog "DBMAME=$DBNAME"
else
  debuglog "using jq..."
  PASSWD="$(cat $WORKINGDIR/dbsettings.json | jq -r '.DBPASSWORD')" && debuglog "PASSWD=****"
  USER="$(cat $WORKINGDIR/dbsettings.json | jq -r '.DBUSER')" && debuglog "USER=$USER"
  DBNAME="$(cat $WORKINGDIR/dbsettings.json | jq -r '.DBNAME')" && debuglog "DBNAME=$DBNAME"
fi
MKTEMP="$($WHICH gmktemp || $WHICH mktemp)" && debuglog "MKTEMP=$MKTEMP"

cleanup() {
  if [ -z $1 ]; then
    abortmsg="Aborting abnormally.  Logfile written to '$LOGFILE'"
  else
    abortmsg="$@"
  fi
  exitstatus="${2:-255}"
  $PRINTF "$abortmsg" > /dev/stderr
  rm -f $TMPFILE
  trap - EXIT
  exit "$exitstatus"
}
trap cleanup EXIT

LOGFILE="$($MKTEMP)" && debuglog "LOGFILE=$LOGFILE"
TMPFILE="$($MKTEMP)" && debuglog "TMPFILE=$TMPFILE"
GIT="$($WHICH git)" && debuglog "GIT=$GIT"
PG_DUMP="$($WHICH pg_dump)" && debuglog "PG_DUMP=$PG_DUMP"
PSQL="$($WHICH psql)" && debuglog "PSQL=$PSQL"
GIT_TAG="$($GIT describe --tags | tail -n1)" && debuglog "GIT_TAG=$GIT_TAG"
