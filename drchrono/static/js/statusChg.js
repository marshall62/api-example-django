/* processing of clicks in the status pulldowns.  First make AJAX call to backend to let it know about
the status change and then we may move the table row to a different row depending on new status.
 */

// menuitem is the dropdown item (a status) that was clicked.
function handleStatusClick ($menuItem) {
  var stat = $menuItem.data('stat');
  var proceed = true;
  if (stat === 'complete')
    proceed = confirm("Proceed with status change to " + $menuItem.text());
  if (proceed) {
    $menuItem.parents(".dropdown").find('.btn').html($menuItem.text() + ' <span class="caret"></span>');
    $menuItem.parents(".dropdown").find('.btn').val($menuItem.data('stat'));
    statusUpdate($menuItem, $menuItem.attr('data-appointment-id'), stat);
  }
}

function statusUpdate (aElt, appointmentId, newStatus) {
  saveStat(appointmentId, newStatus);

  // if status is complete, remove the row and wait for the refresh to put it in the completed table
  var $row = aElt.closest("tr");
  if (newStatus === "complete") {
    $row.remove();
  }
  else if (newStatus === 'waiting') {
    $row.remove();
    alterWaitingRowTime($row);
    moveToTable($row, $('#waitingTableBody'), {'exam': 'In Session', 'absent': 'No Show'}, 'Checked In')
  }
  else if (newStatus === 'exam') {
    $row.remove();
    alterExamRowTime($row); // change the time-waited td to a duration td
    moveToTable($row, $('#examTableBody'), {'complete': 'Complete', 'waiting': 'Checked In'}, 'In Session')
  }
}

/* AJAX to save appointment status to back end */
function saveStat (appt_id, status) {
  var data = new FormData();
  data.set('status',status);
  var url = "/appointments/" + appt_id;
  $.ajax({
    url: url,
    type: "POST",
    data: data,
    processData: false,
    contentType: false,
    error: function (a, b, c) {
      console.log("Failed to write to server! " + a.responseText + b);
      console.log(a);
    },
    success: function (data) {
      console.log("success", data);
    }
  });
}




function alterExamRowTime ($row) {
  // store the cur time as the exam starttime in the row data
  var ts = timestampStr();
  $row.attr('data-exam-starttime', ts);
  // make the time-waited td be a duration td set to 0
  var $td = $row.find('td:nth-child(2)');
  $td.removeAttr('class');
  $td.attr('class', 'duration');
  $td.html('');
}

function alterWaitingRowTime ($row) {
  var ts = timestampStr();
  // store the cur time as the checkin time stored in row data
  $row.attr('data-checkin-time', ts);
  // remove any class on the second td and set to time-waited with nothing in the td yet.
  var $waitTd = $row.find('td:nth-child(2)');
  $waitTd.removeAttr('class');
  $waitTd.attr('class', 'time-waited');
  var sched_time = $row.data('scheduled-time');
  var diff = calcElapsedTime(sched_time);
  if (diff > 0)
    $waitTd.html(toHM(diff));
  else
    $waitTd.html('');
}

function moveToTable ($rowElt, $tbody, menuItems, selectedOption) {
  var appt_id = $rowElt.data('appointment-id');
  var $ddTd = $rowElt.find('td').last();
  $ddTd.empty(); // eliminate the dropdown menu out of the last cell in the row
  var dd = create_status_dropdown(appt_id, selectedOption, menuItems);
  $ddTd.append(dd); // add the cell to the row
  $tbody.append($rowElt); // add the row to table
}

// dropdown menu for status built for an appointment depends on its current status.
// menuItems like: {'waiting': 'Checked In', 'absent': 'No Show'}
function create_status_dropdown (appt_id, selectedOption, menuItems) {
  var dd = '<div class="dropdown">' +
      '              <button class="btn btn-primary dropdown-toggle" type="button" ' +
      '                      data-toggle="dropdown">' + selectedOption +
      '                <span class="caret"></span></button>' +
      '              <ul class="dropdown-menu">';
  // add in the menu items to the dropdown
  for (var [stat, menuLabel] of Object.entries(menuItems))
    dd += '<li><a class="status" data-stat="' +stat+ '" data-appointment-id="' +appt_id+ '">' +menuLabel+ '</a></li>'
  dd += '</ul></div>';
  return dd;
}