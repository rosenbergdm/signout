#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:enc=utf-8
#
# Copyright © 2020-2021 Thomas Butterworth <dmr@davidrosenberg.me>
# Last updated Sat Feb 27 00:13:00 EST 2021
#
# Distributed under terms of the MIT license.

"""
signout/helpers.py
helper functions for MSKCC signout program

"""

import pprint
import re
import sys
from urllib.parse import urljoin, urlparse

from flask import request

from signout.app import application as app

CLEANUP_TIMESTAMP = re.compile(r"\.(..).*$")
SHIFT_TIMES = re.compile(r"^(\d{1,2})(:59:59\.)(.*)$")


def gen_med_sorter(intern_list):
    gen_med = []
    non_gen_med = []
    for i in intern_list:
        if i["name"][0:7] == "Gen Med":
            gen_med.append(i)
        else:
            non_gen_med.append(i)
    gen_med.extend(non_gen_med)
    return gen_med


def format_timestamp(tstamp):
    if tstamp == "None":
        return ""
    return CLEANUP_TIMESTAMP.sub(".\\1", tstamp)


def fix_earlytimes(tstamp):
    if SHIFT_TIMES.match(tstamp):
        hour = str(int(SHIFT_TIMES.sub("\\1", tstamp)) + 1).zfill(2)
        return str(hour) + SHIFT_TIMES.sub(":00:00.\\3", tstamp)
    return tstamp


def cleanup_date_input(dstamp):
    if "-" in dstamp:
        return dstamp
    parts = dstamp.split("/")
    dstamp = "-".join([parts[2], parts[0], parts[1]])
    return dstamp


def dbg(msg):
    if app.config["DEBUG_SIGNOUT_OUTPUT"]:
        pprint.pprint(msg, stream=sys.stderr)


def is_safe_url(target):
    # global request
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


def get_foreground_color(activestate):
    if activestate:
        return "#000000"
    return "#999999"


if __name__ == "__main__":
    pass
