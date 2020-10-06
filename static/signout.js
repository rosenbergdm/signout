// TODO: Refactor all this duplicated code!
//

function displayTime() {
  var today = new Date();
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
  var d = new Date();
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
    // cutoff_time = new Date(Date.UTC(d.getYear() + 1900, d.getMonth(), d.getDate(), 9, 17, 0))
  }
  cutoff_time.setTime(cutoff_time.getTime() + offset * 60 * 10);
  if (date >= cutoff_time) {
    return true;
  } else {
    let hours = Math.floor((cutoff_time - date) / 1000 / 3600);
    let minutes = Math.floor((cutoff_time - date) / 1000 / 60 - 60 * hours);
    let seconds = Math.floor(
      (cutoff_time - date) / 1000 - 60 * minutes - 3600 * hours
    );
    alert(
      `You cannot signout for another ${hours} hours, ${minutes} minutes, and ${seconds} seconds`
    );
    return false;
  }
}

function onCallSubmit() {
  var cutoff_time;
  var d = new Date();
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
    return true;
  } else {
    let hours = Math.floor((cutoff_time - date) / 1000 / 3600);
    let minutes = Math.floor((cutoff_time - date) / 1000 / 60 - 60 * hours);
    let seconds = Math.floor(
      (cutoff_time - date) / 1000 - 60 * minutes - 3600 * hours
    );
    alert(
      `You cannot signout for another ${hours} hours, ${minutes} minutes, and ${seconds} seconds`
    );
    return false;
  }
}
