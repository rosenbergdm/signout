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
# updatedb.sh
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
WORKINGDIR="$($READLINK -f $($DIRNAME $0)/..)"
pushd "$WORKINGDIR"
mkdir -p "$WORKINGDIR/backups" > /dev/null 2>&1
PASSWD="$(cat "$WORKINGDIR/dbsettings.json" | grep pass | sed -e 's#"##g' | awk '{print $2}')"
USER="$(cat $WORKINGDIR/dbsettings.json | grep username | sed -e 's#["|,]##g' | awk '{print $2}')"
DBNAME="$(cat $WORKINGDIR/dbsettings.json | grep dbname | sed -e 's#["|,]##g' | awk '{print $2}')"
TMPFILE="$(mktemp)"
CUR_TAG="$(git describe --tags | tail -n1)"
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

$ECHO "Executing script '$SQLSCRIPT' for DB '$DBNAME' as user '$USER'..."
$ECHO -n "----"
cat $SQLSCRIPT | PGPASSWORD="$PASSWD" psql -U "$USER" "$DBNAME" 2>&1 | tee -a $TMPFILE
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
