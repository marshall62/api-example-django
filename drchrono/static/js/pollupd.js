/* processing that takes place for polling new list of appointments */

/* The AJAX to request the new list */
function getScheduledAppointments () {
  var url = "/appointments/" ;
  $.ajax({
    url: url,
    type: "GET",
    error: function (a, b, c) {
      console.log("Failed to get from server! " + a.responseText + b);
      console.log(a);
    },
    success: function (data) { updateTables(data); }
  });
}


/* update all the tables with appointment data received. */
function updateTables (data) {
  reloadUpcomingTableAppointments(data['upcoming']);
  reloadWaitingTableAppointments(data['waiting']);
  reloadCompletedTableAppointments(data['complete']);
  var avg_wait = data['stats']['avg_wait'];
  var max_wait = data['stats']['max_wait'];
  var avg_duration = data['stats']['avg_duration'];
  addStatsToCompletedTable(avg_wait, max_wait, avg_duration);
  updateExamTableTimes();
}

function addStatsToCompletedTable (avgWait, maxWait, avgDur) {
  var tr = "<tr><td><b>Average Wait time (min):</b></td><td>"+avgWait+"</td>";
  $('#completeTableTbody').append(tr);

  tr = "<tr><td><b>Max Wait time (min):</b></td><td>"+maxWait+"</td>";
  $('#completeTableTbody').append(tr);

  tr = "<tr><td><b>Average Duration (min):</b></td><td>"+avgDur+"</td>";
  $('#completeTableTbody').append(tr);
}


function ratingStars (nStars) {
  var str="";
  if (nStars && nStars > 0 && nStars <= 5) {
    for (var i=0;i<nStars; i++) {
      str += "<img width='30' height='30' src='/static/images/star.png'/>"
    }
    return str;
  }
  return '';
}

function reloadCompletedTableAppointments (appointments) {
  var $tab = $('#completeTableTbody');
  $tab.empty();
  for (var i=0;i<appointments.length;i++) {
    var pa = appointments[i];
    var stars = ratingStars(pa.rating);
    var tr = trTag(pa.appointment_id, pa.scheduled_time, pa.checkin_time);
    tr += "<td>" + pa.completion_time + "</td> <td>" + pa.actual_duration + "</td> <td>" + pa.first_name + "</td> <td>" + pa.last_name + "</td> <td>" + stars + "</td></tr>";
    $tab.append(tr);
  }
}

function waitTimeContent (checkinTime, scheduledTime) {
  var timeSinceCheckin = calcElapsedTime(checkinTime); // TODO Maybe this shouldn't matter.  Ignore showing.
  var timeBehindSchedule = calcElapsedTime(scheduledTime);
  var content = '';
  if (timeBehindSchedule > 0)
    content = waitTimeWithTooltip(toHM(timeBehindSchedule, true), toHM(timeSinceCheckin));
  else
    content = waitTimeWithTooltip(toHM(0), toHM(timeSinceCheckin));
  return content;
}

function reloadWaitingTableAppointments (appointments) {
  var $waitingTab = $('#waitingTableBody');
  $waitingTab.empty();
  for (var i=0;i<appointments.length;i++) {
    var pa = appointments[i];
    // get the wait time
    // var timeBehindSchedule = calcElapsedTime(pa.scheduled_time);
    // var waitTime = '';
    // if (timeBehindSchedule > 0)
    //   waitTime = toHM(timeBehindSchedule, true)
    var wt = waitTimeContent(pa.checkin_time, pa.scheduled_time);
    var ddItems = {'exam': 'In Session', 'absent': 'No Show'}
    var dd = create_status_dropdown(pa.appointment_id, 'Checked In', ddItems);
    var tr = trTag(pa.appointment_id, pa.scheduled_time, pa.checkin_time);
    tr += "<td>" +pa.scheduled_time_12hr+ "</td> <td class='time-waited'>" +wt+ "</td> <td>" +pa.first_name+ "</td> <td>" +pa.last_name+ "</td> <td>" +pa.reason+ "</td> <td>" +dd+ "</td> </tr>";
    $waitingTab.append(tr);
  }
}

function reloadUpcomingTableAppointments(appointments) {
  var $upcomingTab = $('#upcomingAppointmentsTbody');
  $upcomingTab.empty();
  for (var i=0;i<appointments.length;i++) {
    var pa = appointments[i];
    var patientLateTime = calcElapsedTime(pa.scheduled_time);
    var late = '';
    if (patientLateTime > 0)
      late = toHM(patientLateTime);
    var ddItems = {'absent': 'No Show', 'waiting': 'Checked In'}
    var dd = create_status_dropdown(pa.appointment_id, pa.status, ddItems);
    var tr = trTag(pa.appointment_id, pa.scheduled_time);
    tr += "<td>" +pa.scheduled_time_12hr+ "</td> <td>" +late+ "</td> <td>" +pa.first_name+ "</td> <td>" +pa.last_name+ "</td> <td>" +pa.reason+ "</td> <td>" +dd+ "</td> </tr>";
    $upcomingTab.append(tr);
  }

}

function trTag (appt_id, scheduled_time, checkin_time) {
  var r = "<tr data-appointment-id='" + appt_id + "' data-scheduled-time='" + scheduled_time + "'";
  if (checkin_time)
    r += " data-checkin-time='" + checkin_time + "'";
  r += ">";
  return r;
}

