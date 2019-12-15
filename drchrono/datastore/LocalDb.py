from drchrono.datastore.DataStoreAbstract import DataStoreAbstract
from drchrono.models import *
from pickle import dumps,loads
import datetime
import drchrono.dates as dateutil

class LocalDb (DataStoreAbstract):

    def __init__ (self):
        self._patients = Patient.objects.all()
        self._appointments = Appointment.objects.all()
        self._doctor = Doctor.objects.first()

    def save_objects(self, patients, appointments, doctor):
        self.save_appointments(appointments)
        self.save_patients(patients)
        self.save_doctor(doctor)

    def save_appointments (self, appointments):
        Appointment.objects.all().delete()
        for a in appointments:
            Appointment(api_id=a.id, data=dumps(a.data)).save()
        self._appointments = Appointment.objects.all()

    def save_patients (self, patients):
        Patient.objects.all().delete()
        for p in patients:
            Patient(api_id=p.id, data=dumps(p.data)).save()
        self._patients = Patient.objects.all()

    def save_doctor (self, doctor):
        Doctor.objects.all().delete()
        d = Doctor(api_id=doctor.id, data=dumps(doctor.data))
        d.save()
        self._doctor = d

    def _add_api_id (self, record, db_obj):
        record['id'] = db_obj.api_id

    @property
    def doctor (self):
        rec = loads(self._doctor.data)
        self._add_api_id(rec, self._doctor)
        return rec

    @property
    def appointments (self):
        recs = []
        for a in self._appointments:
            r = loads(a.data)
            self._add_api_id(r,a)
            recs.append(r)
        return recs

    @property
    def patients (self):
        recs = []
        for p in self._patients:
            r = loads(p.data)
            self._add_api_id(r, p)
            recs.append(r)
        return recs


    def create_appointment(self, appt_data):
        api_id = appt_data.get('id',-1) # if the API is failing, then there won't be an id in the appt_data and we store -1
        a = Appointment(api_id=api_id, data=dumps(appt_data))
        a.save()
        return appt_data

    def reload_appointments(self):
        self._appointments = Appointment.objects.all()


    def reload_patients(self):
        self._patients = Patient.objects.all()

    def _create_status_transition (self, old_status, new_status, appt_id):
        t = {'from_status': old_status, 'to_status': new_status, 'appointment': appt_id,
             'datetime': dateutil.timestamp_api_format(datetime.datetime.now())}
        return t

    def save_appointment_status(self, appt_id, status):
        # when status changes we need to create a status transitions inside the data.
        a = Appointment.objects.filter(api_id=appt_id).first()
        data = loads(a.data)
        from_status = data['status']
        t = self._create_status_transition(from_status, status, appt_id)
        transitions = data['status_transitions']
        # not sure whats in there if no transitions have happened
        if transitions:
            transitions.append(t)
        else:
            data['status_transitions'] = list(t)
        data['status'] = status
        a.data = dumps(data)
        a.save()

    def save_appointment_extra (self, appt_id, extra):
        a = Appointment.objects.filter(api_id=appt_id).first()
        data = loads(a.data)
        data['extra'] = extra
        a.data = dumps(data)
        a.save()

    def update_patient(self, patient_id, new_data=None):
        p = Patient.objects.filter(api_id=patient_id).first()
        data = loads(p.data)
        data.update(new_data)  # merge in the new data
        p.data = dumps(data)
        p.save()

