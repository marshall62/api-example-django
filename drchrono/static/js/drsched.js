$(document).ready(function() {
  // status dropdown items click handling
  $(document).on('click', '.status', function () {
    handleStatusClick($(this));

  });

  setInterval(updateTimes, 10*1000); // update patient durations and wait times every 10 secs
  setInterval(getScheduledAppointments, 1* 30*1000); // update the schedule every minute.

});