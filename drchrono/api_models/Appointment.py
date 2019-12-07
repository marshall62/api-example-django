from drchrono.endpoints import AppointmentEndpoint
from drchrono.api_models.APIObj import APIObj
from drchrono.api_models.Doctor import Doctor
import datetime
import drchrono.dates as dateutil

class Appointment(APIObj):
    '''
    A single appointment
    '''

    def __init__(self, id=None, doctor=None, duration=0, data={}):
        if not doctor:
            doctor = Doctor()
        if id:
            super().__init__(endpoint=AppointmentEndpoint)
            self.load_by_id(id)
        else:
            super().__init__(data=data, endpoint=AppointmentEndpoint)
            self._data['doctor'] = doctor.id
            self._data['duration'] = duration
            self._data['exam_room'] = 1
            self._data['office'] = doctor.data['office']

    @staticmethod
    def create (patient_id, scheduled_time=None, duration=30, reason='yearly exam'):
        if not scheduled_time:
            scheduled_time = dateutil.timestamp_api_format(datetime.date.today())
        doc = Doctor()
        data = {'patient': patient_id, 'scheduled_time': scheduled_time, 'duration': str(duration), 'reason': reason, 'exam_room': 1, 'office': doc.office, 'doctor': doc.id}
        return APIObj._create(data,Appointment,AppointmentEndpoint)

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

    @reason.setter
    def reason (self, reason):
        self._data['reason'] = reason

    @property
    def duration (self):
        return self._data['duration']

    @duration.setter
    def duration (self, duration):
        self._data['duration'] = duration


    @property
    def status (self):
        return self._data['status']

    # TODO change this.  A setter shouldn't make API call
    @status.setter
    def status (self, status):
        self._data_update_persist('status', status) # persist status change via API

    @property
    def status_transitions (self):
        return self._data['status_transitions']

    @property
    def checkin_time (self):
        for trans in self.status_transitions:
            if trans['to_status'] == 'Checked In':
                return trans['datetime']
        return None

    @property
    def exam_starttime (self):
        for trans in self.status_transitions:
            if trans['to_status'] == 'In Session':
                return trans['datetime']
        return None


    def __repr__ (self):
        if self.status == 'Checked In':
            return "<Appointment {} {} {} @ {}>".format(self.patient_id, self.scheduled_time, self.status, self.checkin_time)
        elif self.status == 'In Session':
            return "<Appointment {} {} {} @ {}>".format(self.patient_id, self.scheduled_time, self.status, self.exam_starttime)
        else:
            return "<Appointment {} {} {}>".format(self.patient_id, self.scheduled_time, self.status)


