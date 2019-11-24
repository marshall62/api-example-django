from drchrono.models import APIObj

class PatientAppointment (APIObj):

    def __init__ (self, patient, appointment):
        self.patient = patient
        self.appointment = appointment

