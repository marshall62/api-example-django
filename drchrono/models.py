from django.db import models

# Keeps track of todays patient's appointments
class PatientAppointment (models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    ssn4 = models.CharField(max_length=4)
    reason = models.CharField(max_length=250, blank=True, null=True)
    health_change = models.CharField(max_length=500, blank=True, null=True)
    expected_duration = models.IntegerField()
    scheduled_time = models.CharField(max_length=5)
    checkin_time = models.TimeField(auto_now=False, blank=True, null=True)
    exam_start_time = models.TimeField(auto_now=False, blank=True, null=True)
    complete_time = models.TimeField(auto_now=False, blank=True, null=True)
    status = models.CharField(max_length=12)
    patient_id = models.IntegerField()
    appointment_id = models.IntegerField()
    patient_changed = models.BooleanField(default=False)
    appointment_changed = models.BooleanField(default=False)



    def __str__(self):
        return self.first_name + " " + self.last_name + ":" + self.status