function nonCallSubmit() {
  // Weekday or weekend
  var cutoff_time;
  var d = new Date();
  if ((d.getDay() == 6) || (d.getDay() == 0)) {
    cutoff_time = Date(Date(d.getYear(), d.getMonth(), d.getDate(), 17, 30, 0))
  } else {
    cutoff_time = Date(Date(d.getYear(), d.getMonth(), d.getDate(), 19, 0, 0))
  }
  if (d > cutoff_time) {
    return true;
  } else {
    alert("It's not yet time to signout");
    return false;
  }
}

function onCallSubmit() {
  var cutoff_time;
  var d = new Date();
  cutoff_time = Date(Date(d.getYear(), d.getMonth(), d.getDate(), 19, 0, 0))
  if (d > cutoff_time) {
    return true;
  } else {
    alert("It's not yet time to signout");
    return false;
  }
}
