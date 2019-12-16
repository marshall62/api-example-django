// return the elapsed time as HH:MM string
function calcElapsedTime (startTime) {
  var ms = Date.now()- Date.parse(startTime);
  // want as minutes
  return Math.round(ms / (60 * 1000));
}

function toHM (mins, addColor=false) {
  var h = Math.floor(mins / 60);
  var mins = mins % 60;
  var res = "";
  if (h >= 1)
    res += h + ":";
  if (mins >= 10)
    res += mins.toString();
  else if (h >= 1)
    res += "0" + mins.toString();
  else
    res += mins.toString();
  if (addColor) {
    var color = 'red';
    if (h < 1 && mins < 20 && mins > 15)
      color = 'orange';
    else if (h < 1 && mins < 15)
      color = 'black';
    return "<font color='" + color + "'>" + res + "</font>"

  }
  else
    return res;

}

function waitTimeWithTooltip (displayedTime, timeSinceCheckin) {
  // return '<div class="tooltip">' + displayedTime +
  //   '<span class="tooltiptext">Time since checkin: ' + timeSinceCheckin + '</span></div>';
  return '<abbr title="Time since check-in: '+ timeSinceCheckin + '">' + displayedTime + '</abbr>';
}

function pad0 (n) {
  return n < 10 ? '0'+n : n;
}

function timestampStr () {
  var ts = new Date();
  var month = ts.getMonth()+1;
  var day = ts.getDate();
  var hr = ts.getHours();
  var mint = ts.getMinutes();
  var sec = ts.getSeconds();

  var monthStr = pad0(month);
  var dayStr = pad0(day);
  var hrStr = pad0(hr);
  var minStr = pad0(mint);
  var secStr = pad0(sec);
  return `${ts.getFullYear()}-${monthStr}-${dayStr}T${hrStr}:${minStr}:${secStr}`

}

function now_hrmin () {
  var n = new Date();
  var hr = n.getHours();
  var mins = n.getMinutes();
  var ampm = 'AM';
  if (hr >= 12) {
    ampm = 'PM';
    hr = hr % 12;
  }
  if (hr == 0)
    hr = 12;
  hr = `${hr}`;
  if (mins == 0)
    mins = '00';
  else if (mins < 10)
    mins = `0${mins}`;
  else
    mins = `${mins}`;

  return `${hr}:${mins} ${ampm}`;
}