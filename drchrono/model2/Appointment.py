class Appointment:

    STATUS_COMPLETE = 'Complete'
    STATUS_WAITING = 'Checked In'
    STATUS_EXAM = 'In Session'
    STATUS_NO_SHOW = 'No Show'
    STATUS_CANCELLED = 'Cancelled'

    def __init__(self, data):
        self._data = data

    @property
    def id (self):
        return self._data['id']

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

    @status.setter
    def status (self, status):
        self._data['status'] = status

    @property
    def status_transitions (self):
        return self._data['status_transitions']

    @property
    def checkin_time (self):
        for trans in self.status_transitions:
            if trans['to_status'] == self.STATUS_WAITING:
                return trans['datetime']
        return None

    @property
    def exam_starttime (self):
        for trans in self.status_transitions:
            if trans['to_status'] == self.STATUS_EXAM:
                return trans['datetime']
        return None


    @property
    def data (self):
        return self._data



    def __repr__ (self):
        if self.status == self.STATUS_WAITING:
            return "<Appointment {} for {} {} {} @ {}>".format(self.id, self.patient_id, self.scheduled_time, self.status, self.checkin_time)
        elif self.status == 'In Session':
            return "<Appointment {} for {} {} {} @ {}>".format(self.id, self.patient_id, self.scheduled_time, self.status, self.exam_starttime)
        else:
            return "<Appointment {} for {} {} {}>".format(self.id, self.patient_id, self.scheduled_time, self.status)


