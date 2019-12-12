
// The .time-waited td holds how long patient has been in waiting rm.  The timestamp of when status became Checked In is
// held in the tr's data-checkin-time.  We compute the time diff between now and checkin time and put this in the time-waited td.
function updateWaitingTableTimes () {
  $('#waitingTableBody tr').each(function () {
    var checkinTime = $(this).data('checkin-time');  // rows in waiting table have checkin-time in yyyy-mm-ddThh:mm:ss format
    var scheduledTime = $(this).data('scheduled-time');  // rows in waiting table have scheduled-time in yyyy-mm-ddThh:mm:ss format
    var wt = waitTimeContent(checkinTime,scheduledTime);
    // show as time-behind-scheduled/time-since-checkin
    $(this).find('.time-waited').html(wt); // set content of the time-waited td to minutes
    // else $(this).find('.time-waited').html('');
  })
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

// The .duration td holds how long patient has been in exam rm.  The timestamp of when status became Checked In is
// held in the tr's data-checkin-time.  We compute the time diff between now and checkin time and put this in the time-waited td.
function updateExamTableTimes () {
  $('#examTableBody tr').each(function () {
    var starttime = $(this).data('exam-starttime');  // rows in exam table have start times in yyyy-mm-ddThh:mm:ss format
    var elapsedTimeMin = calcElapsedTime(starttime);
    var afterSchedTime = toHM(elapsedTimeMin);
    var a = "<a"
    $(this).find('.duration').html(toHM(elapsedTimeMin)); // set content of the duration td to minutes

  })
}

function updateUpcomingTableTimes () {
  $('#upcomingAppointmentsTbody tr').each(function () {
    var schedTime = $(this).data('scheduled-time');
    elapsedTimeMin = calcElapsedTime(schedTime);
    if (elapsedTimeMin > 0)
      $(this).find('.late').html(toHM(elapsedTimeMin)); // set content of the duration td to minutes

  })
}

function updateTimes () {
  console.log("updating times");
  updateWaitingTableTimes();
  updateExamTableTimes();
  updateUpcomingTableTimes();
}