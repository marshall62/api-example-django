from drchrono import dates
class PatientAppointment:

    def __init__ (self, patient, appointment):
        self._patient = patient #type: Patient
        self._appointment = appointment #type: Appointment


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
    def last_name (self):
        return self._patient.last_name

    @property
    def ssn4 (self):
        return self._patient.ssn4

    @property
    def scheduled_time_12hr (self):
        return dates.time_format(self._appointment.scheduled_time)

    @property
    def duration (self):
        return self._appointment.duration

    @property
    def scheduled_time (self):
        return self._appointment.scheduled_time

    @property
    def reason (self):
        return self._appointment.reason

    @property
    def status (self):
        return self.simplify_status(self._appointment.status)

    @status.setter
    def status (self, status):
        self._appointment.status = status # will persist new status to API

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

    def __repr__ (self):
        return "<PatientAppointment {} {} {} {}>".format(self.first_name, self.last_name,self.scheduled_time,self.status)

