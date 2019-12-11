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
function updateTables (patient_appointments) {
  reloadUpcomingTableAppointments(patient_appointments['upcoming']);
  reloadWaitingTableAppointments(patient_appointments['waiting']);
  reloadCompletedTableAppointments(patient_appointments['complete']);
  updateExamTableTimes();
}


function reloadCompletedTableAppointments (appointments) {
  var $tab = $('#completeTableTbody');
  $tab.empty();
  for (var i=0;i<appointments.length;i++) {
    var pa = appointments[i];
    var tr = trTag(pa.appointment_id, pa.scheduled_time, pa.checkin_time);
    tr += "<td>" + "TODO" + "</td> <td>" + "TODO" + "</td> <td>" + pa.first_name + "</td> <td>" + pa.last_name + "</td> <td>" + "5 stars" + "</td></tr>";
    $tab.append(tr);
  }
}

function reloadWaitingTableAppointments (appointments) {
  var $waitingTab = $('#waitingTableBody');
  $waitingTab.empty();
  for (var i=0;i<appointments.length;i++) {
    var pa = appointments[i];
    // get the wait time
    var timeBehindSchedule = calcElapsedTime(pa.scheduled_time);
    var waitTime = '';
    if (timeBehindSchedule > 0)
      waitTime = toHM(timeBehindSchedule, true)
    var ddItems = {'exam': 'In Session', 'absent': 'No Show'}
    var dd = create_status_dropdown(pa.appointment_id, 'Checked In', ddItems);
    var tr = trTag(pa.appointment_id, pa.scheduled_time, pa.checkin_time);
    tr += "<td>" +pa.scheduled_time_12hr+ "</td> <td>" +waitTime+ "</td> <td>" +pa.first_name+ "</td> <td>" +pa.last_name+ "</td> <td>" +pa.reason+ "</td> <td>" +dd+ "</td> </tr>";
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

