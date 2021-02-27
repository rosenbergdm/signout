#! /usr/bin/env bash
#
# backupdb.sh
# Copyright (C) 2020 Thomas Butterworth <dmr@davidrosenberg.me>
#
# Distributed under terms of the MIT license.
#

PG_DUMP="$(which pg_dump)"
GIT_TAG="$(git describe --tags | tail -n1)"
DIRNAME="$(which gdirname || which dirname)"
READLINK="$(which greadlink || which readlink)"
TARGET="$($DIRNAME $0)/../backups/signout-${GIT_TAG}.sql.gz"
WORKINGDIR="$($READLINK -f $($DIRNAME $0)/..)"
mkdir -p "$WORKINGDIR/backups" > /dev/null 2>&1
PASSWD="$(cat "$WORKINGDIR/dbsettings.json" | grep pass | sed -e 's#"##g' | awk '{print $2}')"
USER="$(cat $WORKINGDIR/dbsettings.json | grep username | sed -e 's#["|,]##g' | awk '{print $2}')"
DBNAME="$(cat $WORKINGDIR/dbsettings.json | grep dbname | sed -e 's#["|,]##g' | awk '{print $2}')"
if [ -f "$TARGET" ]; then
  echo "BACKUP FILE $TARGET already exists.  Did you need to bump the git tag first?"
  exit 255
else
  PGPASSWORD="$PASSWD" $PG_DUMP "$DBNAME" -U "$USER" | gzip - - > "${TARGET}"
  echo "Backed up database to file $TARGET"
fi



# vim: ft=sh
