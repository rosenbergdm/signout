// /usr/bin/env node
// -*- coding: utf-8 -*-
// vim:enc=utf-8
//
//    This file is part of signout.py the house staff web-based signout
//    manager for MSKCC.
//    Copyright © 2020-2021 David M. Rosenberg <dmr@davidrosenberg.me>
//
//    This program is free software: you can redistribute it and/or modify
//    it under the terms of the GNU General Public License as published by
//    the Free Software Foundation, either version 3 of the License, or
//    (at your option) any later version.
//
//    This program is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU General Public License for more details.
//
//    You should have received a copy of the GNU General Public License
//    along with this program.  If not, see <https://www.gnu.org/licenses/>.
//
// static/signout.js
// MSKCC signout.py javascript library

//{{{ Global variables and initialization

// set to DEBUG_SIGNOUT_JS = 1 to show extra console logging info
var DEBUG_SIGNOUT_JS = 0;
// time difference in ms between client and server
var timeoffset = 0;
var timesyncXhr = new XMLHttpRequest();
var signoutInProgress = false;

//}}}

//{{{ Helper functions
var insertContact = function () {
  var contact = document.getElementById("contact");
  contact.href = "mailto:" + "support" + "@" + "davidrosenberg.me";
  contact.text = "support" + "@" + "davidrosenberg.me";
};

var checkIe = function () {
  var ua = window.navigator["userAgent"];
  var is_msie = 0;

  if (ua.indexOf("MSIE")) {
    is_msie = 1;
  }

  if (ua.indexOf("Trident") > 0) {
    is_msie = 1;
  }

  if (is_msie > 0) {
    alert("IS MSIE");
  }
  return ua;
};

// 0 pad on the left to left
var padLeft = function (i) {
  return ("0" + i).slice(-2);
};

// 0 pad right
var padright = function (i) {
  return (i + "000").substring(0, 3);
};

var runTimesyncOnLoad = function () {
  displayTime();
  updateTimeSync();
  // Re-sync time and calc offset every 15 seconds
  setInterval(updateTimeSync, 15000);
};

//}}}

//{{{ Manage NF signout progression
/* Limit action to the signout initiated by NF and make it visible */
var startsignout = function (internid) {
  var startSignout = new XMLHttpRequest();
  startSignout.addEventListener("load", function () {
    var response_message = JSON.parse(this.responseText);
    if (response_message.status == "ERROR") {
      alert("Error logging start time for id '" + response_message.id + "'");
    }
  });
  startSignout.open("GET", "/start_signout?id=" + internid);
  startSignout.send();
  var this_signout = document.getElementsByClassName("intern_" + internid)[0];
  signoutInProgress = true;
  for (var i = this_signout.children.length - 1; i >= 0; i--) {
    this_signout.children[i].outerHTML =
      "<td style='color:blue;'>" + this_signout.children[i].innerText + "</td>";
  }
  var sbuttons = document.getElementsByClassName("startbutton");
  for (i = 0; i <= sbuttons.length - 1; i++) {
    sbuttons[i].disabled = true;
  }
};

var safe_refresh = function () {
  if (!signoutInProgress) {
    window.location.reload();
  }
};
//}}}

//{{{ Time syncing

// Given a server-issued timestamp, update the timesync (offset) variable
var updateTimeOffset = function (timestring) {
  var splittimestring = timestring.split(":");
  var splitms = splittimestring[2].split(".");
  var localtime = new Date(Date.now());
  var remotetime = new Date(Date.now());
  remotetime.setHours(
    Number(splittimestring[0]),
    Number(splittimestring[1]),
    Number(splitms[0]),
    Number(splitms[1])
  );
  timeoffset = remotetime - localtime;
  if (DEBUG_SIGNOUT_JS == 1) {
    console.log("time offset is " + timeoffset + " ms");
  }
};

// Request the time from server, and update the timesync var with resposne
var updateTimeSync = function () {
  timesyncXhr = new XMLHttpRequest();
  timesyncXhr.addEventListener("load", function () {
    if (DEBUG_SIGNOUT_JS == 1) {
      console.log("time received from server:  " + this.responseText);
    }
    updateTimeOffset(this.responseText);
  });
  timesyncXhr.open(
    "GET",
    // "/synctime?cachefix=" + String(Math.random()).substr(2, 10)
    "/synctime"
  );
  timesyncXhr.send();
};

// update the running clocks (top and each section) every 19 ms
var displayTime = function () {
  var today = new Date(Date.now() + timeoffset);
  var h = today.getHours();
  var m = today.getMinutes();
  var s = today.getSeconds();
  var ms = padright(today.getMilliseconds());
  m = padLeft(m);
  s = padLeft(s);
  document.getElementById("runningclock").innerHTML =
    '<h3 text-align="left;">Current Time: ' +
    h +
    ":" +
    m +
    ":" +
    s +
    "." +
    ms +
    "</h3></br>";
  // Increment time every 19 ms (chosen because relatively prime to 1000 = 1 s)
  setTimeout(displayTime, 19);
  var i;
  var clocks = document.getElementsByClassName("runningclock");
  for (i = 0; i < clocks.length; i++) {
    clocks[i].innerHTML = "Time: " + h + ":" + m + ":" + s + "." + ms;
  }
};
//}}}

//{{{ Execute submission

// function submitSignout(on_call = false) {
var submitSignout = function (on_call) {
  var cutoff_time;
  var d = new Date(Date.now() + timeoffset);
  var date = new Date(
    Date.UTC(
      d.getYear() + 1900,
      d.getMonth(),
      d.getDate(),
      d.getHours(),
      d.getMinutes(),
      d.getSeconds()
    )
  );
  var offset = date.getTimezoneOffset();
  date.setTime(date.getTime() + offset * 60 * 10);
  if (d.getDay() == 6 || d.getDay() == 0 || on_call) {
    cutoff_time = new Date(
      Date.UTC(d.getYear() + 1900, d.getMonth(), d.getDate(), 19, 0, 0)
    );
  } else {
    cutoff_time = new Date(
      Date.UTC(d.getYear() + 1900, d.getMonth(), d.getDate(), 17, 30, 0)
    );
  }
  cutoff_time.setTime(cutoff_time.getTime() + offset * 60 * 10);
  var allow_signout = date >= cutoff_time;
  if (DEBUG_SIGNOUT_JS == 1) {
    allow_signout = true;
  }
  if (allow_signout) {
    let timestamp = new Date(Date.now());
    let hosttimestamps = document.getElementsByName("hosttimestamp");
    for (var i = hosttimestamps.length - 1; i >= 0; i--) {
      hosttimestamps[i].value = timestamp;
    }
    return true;
  } else {
    let hours = Math.floor((cutoff_time - date) / 1000 / 3600);
    let minutes = Math.floor((cutoff_time - date) / 1000 / 60 - 60 * hours);
    let seconds = Math.floor(
      (cutoff_time - date) / 1000 - 60 * minutes - 3600 * hours
    );
    alert(
      "You cannot signout for another " +
        hours +
        " hours, " +
        minutes +
        " minutes, and " +
        seconds +
        " seconds"
    );
    return false;
  }
};
//}}}

// vim: ft=javascript fenc=utf-8:
