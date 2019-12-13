import drchrono.sched.ModelObjects
from drchrono.api_models.PatientAppointment import PatientAppointment

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


    def get_patient_appointments (self, patient_id=None):
        '''
        :return: List[PatientAppointment] objects for today sorted by scheduled time
        '''
        patient_id = int(patient_id) if patient_id else None
        m = drchrono.sched.ModelObjects.ModelObjects()

        res = []
        pas = m.appointments #type: List[PatientAppointment]
        for a in pas:
            pid = a.patient_id
            if patient_id and pid != patient_id:
                continue
            p = m.patients_map[pid]
            pa = PatientAppointment(patient=p, appointment=a)
            res.append(pa)
        return sorted(res, key=lambda pa: pa.scheduled_time)


