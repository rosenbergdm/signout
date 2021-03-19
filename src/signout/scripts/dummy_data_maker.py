#!/usr/bin/env python3
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

"""
dummy_data_builder.py
Builds temporary data for the testing server for people to see
and manipulate

"""
import random

names = [
    "Yuri Youngren",
    "Agripina Abboud",
    "Delois Dahle",
    "Brynn Beal",
    "Youlanda Yates",
    "Elene Erby",
    "Armandina Aquilino",
    "Lakeisha London",
    "Nina Norsworthy",
    "Dina Donaldson",
    "Nadine Newson",
    "Anisha Andersen",
    "Karon Kinkel",
    "Luetta Luedke",
    "Tracy Tseng",
    "Marquis Moldenhauer",
    "Marisol Montelongo",
    "Antonina Andre",
    "Hilma Harps",
    "Linnea Loftus",
    "Alexa Antley",
    "Annelle Arreola",
    "Ghislaine Guadalupe",
    "Alysa Appling",
    "Jacinta Joynes",
    "Maragret Muncy",
    "Mel Munguia",
    "Holley Hillard",
    "Tamie Tootle",
    "Wally Wingler",
    "Boyd Blalock",
    "Sherryl Silvis",
    "Penny Parrilla",
    "Myrta Mund",
    "Kanesha Karls",
    "Doyle Dobyns",
    "Rubi Rehberg",
    "Deon Dona",
    "Shalanda Salais",
    "Mara Mascarenas",
    "Monserrate Moreles",
    "Kaley Knouse",
    "Babara Brogan",
    "Naoma Neale",
    "Lenard Lukasiewicz",
    "Nanci Nagler",
    "Marianna Mcgough",
    "Nichol Nickles",
    "Diana Deborde",
    "Elaine Easterling",
]


def build_entry(oncall=False):
    global names
    entryname = random.choice(names)
    names.remove(entryname)
    entrycallback = "x" + str(random.randrange(1000, 9999))
    entryservice = str(random.randrange(1, 40))
    entryaddtime = (
        "current_timestamp + interval '%s minutes' + interval '%s seconds'"
        % (str(random.randrange(1, 60)), str(random.randrange(1, 60)))
    )
    entryoncall = "FALSE"
    if oncall:
        entryoncall = "TRUE"
        entryaddtime = entryaddtime + " + interval '1 hour'"
    querystring = """
        INSERT INTO signout (intern_name, intern_callback, service, oncall, addtime)
        VALUES ('%s', '%s', '%s', %s, %s);
        """ % (
        entryname,
        entrycallback,
        entryservice,
        entryoncall,
        entryaddtime,
    )
    if __name__ == "__main__":
        print(querystring)
    return querystring


if __name__ == "__main__":
    for x in range(13):
        build_entry()
    for x in range(7):
        build_entry(oncall=True)
