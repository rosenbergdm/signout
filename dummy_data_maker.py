#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Thomas Butterworth <dmr@davidrosenberg.me>
#
# Distributed under terms of the MIT license.

"""
dummy_data_builder.py
Builds temporary data for the testing server for people to see 
and manipulate

"""
import random

names = [
    "Kara Thrace", "Nancie Hogg", "Jeri Sherrard", "Moises Newsom", "Gearldine Foxworth",
    "Serina Lacomb", "Obdulia Delorenzo", "Meghan Beatson", "Lavada Golay", "Marnie Frith",
    "Trena Cressey", "Hermelinda Mullikin", "Cherly Caso", "Ola Torres",
    "Jacalyn Crews", "Piper Rolan-Adeyemi", "Lezlie Judd", "Marchelle Goode",
    "Evonne Granda", "Arlie Ditzler", "Carl Silverberg", "Sharolyn Erb",
    "Marg Brazelton", "Ericka Billups", "Claudia Philips", "Thomas Butterworth",
    "Dawna Cost", "Willodean Delafuente", "Youlanda Zajicek", "Gwenn Arnold"]


def build_entry():
    """build a randomly timed db entry from the names set above

    :function: TODO
    :returns: TODO

    """
    entryname = random.choice(names)
    names.remove(entryname)
    entrycallback = "x" + str(random.randrange(1000, 9999))
    entryservice = str(random.randrange(1, 33))
    entryaddtime = "current_timestamp + interval '%s minutes' + interval '%s seconds'" % (str(random.randrange(1, 60)), str(random.randrange(1, 60)))
    entryoncall = "TRUE"
    if random.random() < 0.3:
        entryoncall = "FALSE"
    querystring = """INSERT INTO signout (intern_name, intern_callback, service, oncall, addtime) VALUES ('%s', '%s', %s, %s, %s);""" % (entryname, entrycallback, entryservice, entryoncall, entryaddtime)
    print(querystring)

if __name__ == "__main__":
    for x in range(20):
        build_entry()

