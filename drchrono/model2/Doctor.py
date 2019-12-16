import drchrono.sched.ModelObjects
from drchrono.model2.PatientAppointment import PatientAppointment

class Doctor:

    def __init__ (self, data):
        self._data = data

    @property
    def id (self):
        return self._data['id']

    @property
    def data (self):
        return self._data

    @property
    def first_name (self):
        return self._data['first_name']

    @property
    def last_name (self):
        return self._data['last_name']

    @property
    def office (self):
        return self._data['office']





