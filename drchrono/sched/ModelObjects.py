from drchrono.datastore.APIGateway import APIGateway
from drchrono.datastore.LocalDb import LocalDb
from drchrono.model2.Doctor import Doctor
from drchrono.model2.Appointment import Appointment
from drchrono.model2.Patient import Patient
import threading

import traceback

class ModelObjects:

    instance = None
    show_stack_trace = False
    lock = threading.Lock()

    def __new__(cls, load_local=False, load_api=True):
        # construction is rather slow because of the api query so I check/set a flag rather than rely on the slower instance
        # (in lieu of critical section w Lock) which would better
        ModelObjects.lock.acquire()
        try:
            if not ModelObjects.instance:
                ModelObjects.instance = ModelObjects.__ModelObjects(load_local, load_api)
            return ModelObjects.instance
        finally:
            ModelObjects.lock.release()


    class __ModelObjects:

        def __init__ (self, load_local, load_api):
            try:
                if load_api:
                    # loading from the API dumps what comes back to the local db
                    self._load_from_api()
                    # put the stuff that came from API into DB
                    self.local_db = LocalDb()
                    self.local_db.save_objects(self._patients, self._appointments, self._doctor)
                # running from local requires api first (which dumps to db) and then will set
                # the db to be where stuff comes from.
                if load_local:
                    self.local_db = LocalDb()
                    self._load_from_local()

            # If there's a failure loading from the API, load from the db
            except Exception as e:
                print("Failed to load from API.  Loading from DB")
                self.prexc()
                self.local_db = LocalDb()
                self._load_from_local()

        def _load_from_api (self):
            self.api_gateway = APIGateway()
            office = self.api_gateway.office
            drrec = self.api_gateway.doctor
            drrec['office'] = office['id'] # We only need the office id in the doctor
            self._doctor = Doctor(drrec)
            self._load_patients(self.api_gateway)
            self._load_appointments(self.api_gateway)


        def _load_from_local (self):

            self._doctor = Doctor(self.local_db.doctor)

            pats = self.local_db.patients
            self._patients = []
            self._patients_map = {}
            for p in pats:
                pat = Patient(data=p)
                self._patients.append(pat)
                self._patients_map[pat.id] = pat

            apts = self.local_db.appointments
            self._appointments = []
            self._appointments_map = {}
            for a in apts:
                apt = Appointment(data=a)
                self._appointments.append(apt)
                self._appointments_map[apt.id] = apt


        @property
        def doctor(self):
            return self._doctor

        @property
        def patients(self):
            return self._patients

        @property
        def patients_map (self):
            return self._patients_map

        @property
        def appointments(self):
            return self._appointments

        @property
        def appointments_map (self):
            return self._appointments_map

        def reload_patients (self):
            try:
                self.api_gateway.reload_patients()
                self._load_patients(self.api_gateway)
            except Exception as e:
                print("Failed to reload patients from api.  Going with DB")
                self.prexc()
                self.local_db.reload_patients()
                self._load_patients(self.local_db)
            else:  # when successful reload from API, put in the db.
                self.local_db.save_patients(self._patients)

        def _load_patients (self, data_store):
            self._patients = list(map(Patient, data_store.patients))
            self._patients_map = {int(p.id): p for p in self._patients}


        def reload_appointments (self):
            '''
            refresh the appointments.  Get from API.  If that fails, get from DB
            :return:
            '''
            try:
                self.api_gateway.reload_appointments()
                self._load_appointments(self.api_gateway)
            except Exception as e:
                print("Failed to reload appointments from api.  Going with DB")
                self.prexc()
                self.local_db.reload_appointments()
                self._load_appointments(self.local_db)
            else:  # when successful reload from API, put in the db.
                self.local_db.save_appointments(self._appointments)

        def _load_appointments (self, data_store):
            self._appointments = list(map(Appointment, data_store.appointments))
            self._appointments_map = {int(a.id): a for a in self._appointments}


        def create_appointment (self, appointment):
            self._appointments.append(appointment)
            try:
                rec = self.api_gateway.create_appointment(appointment.data)
            except Exception as e:
                # TODO if the API fails we'll create an appointment with a negative api-id so that we can
                # tell it needs to be created in the API later.
                self.prexc()
                rec = self.local_db.create_appointment(appointment.data)
            apt = Appointment(rec)
            self._appointments.append(apt)
            self._appointments_map[apt.id] = apt
            return apt

        def save_appointment_status(self, appointment_id, status):
            try:
                self.api_gateway.save_appointment_status(appointment_id, status)
            except Exception as e:
                print("Failed to set status in api", appointment_id, status)
                self.prexc()
            # write to db no matter what
            self.local_db.save_appointment_status(appointment_id, status)

        def set_extra (self, appointment_id, extra):
            try:
                self.api_gateway.save_appointment_extra(appointment_id, extra)
            except Exception as e:
                print("Failed to save rating", appointment_id, extra)
                self.prexc()
            self.local_db.save_appointment_extra(appointment_id, extra)

        # not using
        def save_patient_summary (self, patient):
            self.api_gateway.update_patient_summary(patient.data)

        def save_patient (self, patient, new_data=None):
            if new_data:
                try:
                    self.api_gateway.update_patient(patient_id=patient.id, new_data=new_data)
                except Exception as e:
                    self.prexc()
                # write patient changes to the db no matter what
                self.local_db.update_patient(patient_id=patient.id, new_data=new_data)

        def prexc (cls):
            if ModelObjects.show_stack_trace:
                traceback.print_exc()



