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
  seq $1 | parallel -I% --max-args 1 curl --silent -X POST -F intern_name=StressTestUser% -F 'intern_callback=1234' -F 'service=1' -F 'oncall=FALSE' -F 'submit=""' >/dev/null 2>&1
fi



# vim: ft=sh
