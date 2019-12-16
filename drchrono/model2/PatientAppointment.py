from drchrono import dates as dateutil
from drchrono.model2.Appointment import Appointment


class PatientAppointment:

    def __init__ (self, patient, appointment):
        self._patient = patient #type: Patient
        self._appointment = appointment #type: Appointment
        self._extra = {}


    @property
    def patient (self):
        return self._patient

    @property
    def appointment (self):
        return self._appointment

    @property
    def patient_id (self):
        return self._patient.id

    @property
    def appointment_id (self):
        return self._appointment.id

    @property
    def first_name (self):
        return self._patient.first_name

    @property
    def nick_name(self):
        return self._patient.nick_name

    @property
    def last_name (self):
        return self._patient.last_name

    @property
    def ssn4 (self):
        return self._patient.ssn4

    @property
    def scheduled_time_12hr (self):
        return dateutil.time_format(self._appointment.scheduled_time)

    @property
    def duration (self):
        return self._appointment.duration

    @property
    def checkin_time (self):
        return self._appointment.checkin_time

    @property
    def exam_starttime (self):
        return self._appointment.exam_starttime

    @property
    def scheduled_time (self):
        return self._appointment.scheduled_time

    @property
    def reason (self):
        return self._appointment.reason

    @property
    def exam_room (self):
        return self._appointment.exam_room

    @property
    def status (self):
        return self.simplify_status(self._appointment.status)

    @status.setter
    def status (self, status):
        self._appointment.status = status # will persist new status to API

    @property
    def completion_time (self):
        t = self.completion_time_raw
        if t:
            return dateutil.time_format(t)
        return None

    @property
    def completion_time_raw (self):
        compl_rec = self._appointment.get_status_transition(Appointment.STATUS_COMPLETE)
        if not compl_rec:
            return None
        t = compl_rec['datetime']
        return t

    # for a completed appointment, get the diff between completion time and time of exam
    @property
    def actual_duration (self):
        res = self.actual_duration_raw
        # replace below with call to dates.hrminsec
        if res != None:
            min, sec = res
            if sec and sec > 9:
                return "{}:{}".format(min,sec)
            elif sec:
                return "{}:0{}".format(min,sec)
            else: return "{}:00".format(min)
        else:
            return ""

    @property
    def actual_duration_raw (self):
        # status history is only stored as low-level json in the gateway cache (not in Model objects)
        compl_rec = self._appointment.get_status_transition(Appointment.STATUS_COMPLETE)
        if not compl_rec:
            return None
        ex_rec = self._appointment.get_status_transition( Appointment.STATUS_EXAM)
        if compl_rec and ex_rec:
            min, sec = dateutil.time_diff(compl_rec['datetime'], ex_rec['datetime'])
            return (min, sec)
        else:
            return (0, 0)

    # extra is a field where I store data that are not supported in the API.  The value will be a
    # dictionary of properties.
    @property
    def extra (self):
        return self._appointment.data.get('extra')

    @extra.setter
    def extra (self, extra):
        self._extra = extra
        # also put in the appointment which allows this to persist throughout the session
        # an overwrite of the extra data is done for now.  It should ADD to it.
        self.appointment.data['extra'] = extra

    @property
    def rating (self):
        return self.extra.get('rating') if self.extra else None

    def is_active (self):
        return self.status != Appointment.STATUS_COMPLETE and self.status != Appointment.STATUS_CANCELLED

    def simplify_status (self, status):
        '''
        This office only cares about statuses:  Checked In, In Session, Complete, No Show.
        Not sure what to make of these: '', Cancelled, Rescheduled, Not Confirmed, Confirmed
           Arrived = Checked In,  In Room = In Session
        '''
        if status == 'Arrived':
            return 'Checked In'
        elif status == 'In Room':
            return 'In Session'
        else:
            return status

    def toJSON (self):
        return {'first_name': self.first_name, 'last_name': self.last_name, 'nick_name': self.nick_name,
                'scheduled_time_12hr': self.scheduled_time_12hr, 'scheduled_time': self.scheduled_time,
                'reason': self.reason, 'status': self.status, 'checkin_time': self.checkin_time,
                'completion_time': self.completion_time, 'actual_duration': self.actual_duration,
                'rating': self.rating, 'exam_room': self.exam_room, 'exam_starttime': self.exam_starttime,
                'appointment_id': self.appointment_id}

    def short_repr (self):
        return "<PA {} {} {} {}>".format(self.first_name, self.last_name, self.scheduled_time_12hr, self.status)

    def __repr__ (self):
        return "<PatientAppointment {} {} {} {}>".format(self.first_name,self.last_name,self.scheduled_time, self.status)

