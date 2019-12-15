from django.db import models

class Patient (models.Model):
    api_id = models.IntegerField(default=1)
    data = models.BinaryField()

class Appointment (models.Model):
    api_id = models.IntegerField(default=1)
    data = models.BinaryField()

class Doctor (models.Model):
    api_id = models.IntegerField(default=1)
    data = models.BinaryField()

