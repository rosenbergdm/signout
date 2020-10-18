// TODO: Refactor all this duplicated code!

/* For the start-stop of signout on the nightfloat page */
function startsignout(internid) {
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
  for (var i = this_signout.children.length - 1; i >= 0; i--) {
    this_signout.children[i].outerHTML =
      "<td style='color:blue;'>" + this_signout.children[i].innerText + "</td>";
  }
  var startbutton = document.getElementById(internid).children[1];
  startbutton.disabled = true;
}

/* For syncing time between clients and the server on the submission and 
 * submission_weekend pages */

var timeoffset = 0;
function updateTimeOffset(timestring) {
  var splittimestring = timestring.split(":");
  var localtime = new Date(Date.now());
  var remotetime = new Date(Date.now());
  remotetime.setHours(
    Number(splittimestring[0]),
    Number(splittimestring[1]),
    Number(splittimestring[2])
  );
  timeoffset = remotetime - localtime;
  console.log("time offset is " + timeoffset);
}

var timesyncXhr = new XMLHttpRequest();
timesyncXhr.addEventListener("load", function () {
  updateTimeOffset(this.responseText);
});
timesyncXhr.open("GET", "/synctime");
timesyncXhr.send();

function displayTime() {
  var today = new Date(Date.now() + timeoffset);
  var h = today.getHours();
  var m = today.getMinutes();
  var s = today.getSeconds();
  m = checkTime(m);
  s = checkTime(s);
  document.getElementById("runningclock").innerHTML =
    "<h3>Current Time: " + h + ":" + m + ":" + s + "</h3></br>";
  setTimeout(displayTime, 100);
}

function checkTime(i) {
  if (i < 10) {
    i = "0" + i;
  }
  return i;
}

function nonCallSubmit() {
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

  if (d.getDay() == 6 || d.getDay() == 0) {
    cutoff_time = new Date(
      Date.UTC(d.getYear() + 1900, d.getMonth(), d.getDate(), 19, 0, 0)
    );
  } else {
    cutoff_time = new Date(
      Date.UTC(d.getYear() + 1900, d.getMonth(), d.getDate(), 17, 30, 0)
    );
  }
  cutoff_time.setTime(cutoff_time.getTime() + offset * 60 * 10);
  if (date >= cutoff_time) {
  // if (true) {
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
}

function onCallSubmit() {
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

  cutoff_time = new Date(
    Date.UTC(d.getYear() + 1900, d.getMonth(), d.getDate(), 19, 0, 0)
  );
  cutoff_time.setTime(cutoff_time.getTime() + offset * 60 * 10);
  if (date >= cutoff_time) {
  // if (true) {
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
}
