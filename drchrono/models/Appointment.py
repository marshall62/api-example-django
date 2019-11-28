from drchrono.endpoints import AppointmentEndpoint
from drchrono.models.APIObj import APIObj
from drchrono.models.Doctor import Doctor

class Appointment(APIObj):
    '''
    A single appointment
    '''

    def __init__(self, doctor=None, duration=0, data={}):
        super().__init__(data=data, endpoint=AppointmentEndpoint)
        if not doctor:
            doctor = Doctor()
        self._data['doctor'] = doctor.id
        self._data['duration'] = duration
        self._data['exam_room'] = 1
        self._data['office'] = doctor.data['office']

    @property
    def patient_id (self):
        return self._data['patient']

    @patient_id.setter
    def patient_id (self, patient_id):
        self.data['patient'] = patient_id

    @property
    def scheduled_time (self):
        return self._data['scheduled_time']

    @scheduled_time.setter
    def scheduled_time (self, scheduled_time):
        self.data['scheduled_time'] = scheduled_time

    @property
    def reason (self):
        return self._data['reason']

    @property
    def status (self):
        return self._data['status']

    @status.setter
    def status (self, status):
        self._data_update_persist('status', status) # persist status change via API


    def __repr__ (self):
        return "<Appointment {} {} {}>".format(self.patient_id, self.scheduled_time, self.status)


