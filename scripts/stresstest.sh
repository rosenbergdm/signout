#!/usr/bin/env bash
#
# stresstest.sh
# Copyright (C) 2020 Thomas Butterworth <dmr@davidrosenberg.me>
#
# Distributed under terms of the MIT license.
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
