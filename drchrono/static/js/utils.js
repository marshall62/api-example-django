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

function timestampStr () {
  var ts = new Date();
  var month = ts.getMonth()+1;
  var day = ts.getDate();
  var monthStr = month < 10 ? `0${month}` : `${month}`;
  var dayStr = day < 10 ? `0${day}` : `${day}`;
  return `${ts.getFullYear()}-${monthStr}-${dayStr}T${ts.getHours()}:${ts.getMinutes()}:${ts.getSeconds()}`

}