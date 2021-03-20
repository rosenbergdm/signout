#!/usr/bin/env bash
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
# stresstest.sh
#
source $HOME/.bashrc

uname -a | grep Darwin >/dev/null && set_perl homebrew

usage() {
  cat<<-EOF
  USAGE:
    > $0 NUM_REQUESTS SUBMISSIONURL
EOF
}

if [ $# -lt 2 ]; then
  usage
  exit 255
else
  echo "Stress testing $2 with $1 simultaneous submissions"
  seq $1 | parallel -I%  -j5 "curl --silent -X POST -F hosttimestamp='Sat Feb 27 2021 21:43:08 GMT-0500 (Eastern Standard Time)' -F intern_callback=1234 -F intern_name=Thomas% -F oncall=FALSE -F service=1 '$2' 2>&1 > /dev/null"
fi


# vim: ft=sh
