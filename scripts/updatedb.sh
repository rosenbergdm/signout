#! /bin/sh
#
# updatedb.sh
# Copyright (C) 2021 Thomas Butterworth <dmr@davidrosenberg.me>
#
# Distributed under terms of the MIT license
#

usage() {
  echo -e "\n\n"
  echo "    > $0 SQL_SCRIPT"
  echo ""
  echo "Upgrade the working signout database schema.  Please include a valid upgrade sql script."
  echo -e "\n\n"
}

ECHO=$(which gecho || which echo)
READLINK=$(which greadlink || which readlink)
DIRNAME=$(which gdirname || which dirname)
if [ -z "$1" ]; then
  $ECHO "SQL UPGRADE SCRIPT REQUIRED"
  usage
  exit 1
fi
if [ ! -e "$1" ]; then
  $ECHO "FILE NOT FOUND"
  usage
  exit 1
fi

SQLSCRIPT="$($READLINK -f $1)"
WORKINGDIR=$($READLINK -f "$($DIRNAME $0)/..")
PASSWD="$(cat "$WORKINGDIR/dbsettings.json" | grep pass | sed -e 's#"##g' | awk '{print $2}')"
USER="$(cat $WORKINGDIR/dbsettings.json | grep username | sed -e 's#["|,]##g' | awk '{print $2}')"
DBNAME="$(cat $WORKINGDIR/dbsettings.json | grep dbname | sed -e 's#["|,]##g' | awk '{print $2}')"
TMPFILE=$(mktemp)
CUR_TAG="$(git tag | tail -n1)"
NEW_TAG="$CUR_TAG""-pre-upgrade"
git tag "$NEW_TAG"

$ECHO "Backing up first... executing $WORKINGDIR/scripts/backupdb.sh with temporary tag $NEW_TAG"
$ECHO -n "----"
$WORKINGDIR/scripts/backupdb.sh
if [ "$?" -gt 0 ]; then
  $ECHO "FAILED! Aborting"
  rm $TMPFILE
  git tag -d "$NEW_TAG"
  exit 3
else
  $ECHO "Backup DONE"
fi

$ECHO "Executing script '$SQLSCRIPT' for DB '$DBNAME' as user '$DB'..."
$ECHO -n "----"
cat $SQLSCRIPT | PGPASSWORD="$PASSWD" psql -U "$DBUSER" "$DBNAME" 2>&1 | tee -a $TMPFILE
if $(grep ERROR $TMPFILE 2>&1 > /dev/null); then
  $ECHO "FAILED to execute '$SQLSCRIPT', please roll back to 'backups/$NEW_TAG.sql.tar.gz' and delete the temp tag"
  rm $TMPFILE
  exit 2
else
  $ECHO "SUCCESS.  Cleaning up."
  rm $TMPFILE
  git tag -d "$NEW_TAG"
fi



# vim: ft=sh
