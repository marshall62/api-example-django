from .APIGateway import APIGateway
from drchrono.model2.Doctor import Doctor
from drchrono.model2.Appointment import Appointment
from drchrono.model2.Patient import Patient

class ModelObjects:

    instance = None

    def __new__(cls):
        if not ModelObjects.instance:
            ModelObjects.instance = ModelObjects.__ModelObjects()
        return ModelObjects.instance

    class __ModelObjects:

        def __init__ (self):
            self.api_gateway = APIGateway()
            office = self.api_gateway.office
            drrec = self.api_gateway.doctor
            drrec['office'] = office['id'] # We only need the office id in the doctor
            self._doctor = Doctor(drrec)
            self._load_patients()
            self._load_appointments()


        @property
        def doctor(self):
            return Doctor(self.api_gateway.doctor)

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
            self.api_gateway.reload_patients()
            self._load_patients()

        def _load_patients (self):
            self._patients = list(map(Patient, self.api_gateway.patients))
            self._patients_map = {p.id: p for p in self._patients}


        def reload_appointments (self):
            self.api_gateway.reload_appointments()
            self._load_appointments()

        def _load_appointments (self):
            self._appointments = list(map(Appointment, self.api_gateway.appointments))
            self._appointments_map = {a.id: a for a in self._appointments}


        # TODO methods below should go into some inner classes for Appointments and Patients

        # write the appointment to the api.  It will not have an id
        def save_appointment (self, appointment):
            rec = self.api_gateway.create_appointment(appointment.data)
            apt = Appointment(rec)
            self.appointments.append(apt)
            self.appointments_map[apt.id] = apt
            return apt


        def set_appointment_status(self, appointment_id, status, persist=False):
            '''
            Modifies the Appointment object held here which also modifies its underlying data dictionary held in
            the APIGateway cache.
            :param appointment_id:
            :param status:
            :param persist: If True, the status will be written to the API
            :return:
            '''
            appt = self._appointments_map[appointment_id] #type: Appointment
            appt.status = status
            if persist:
                self.api_gateway.save_appointment_stat(appointment_id)


        def get_patients_from_name(self, fname, lname, ssn4=None):
            l = []
            for p in self.patients:
                if p.first_name.lower() == fname.lower() and p.last_name.lower() == lname.lower():
                    if ssn4 and p.ssn4 == ssn4:
                        l.append(p)
                    elif not ssn4:
                        l.append(p)
            return l

        def get_patient_by_id (self, id):
            return self.patients_map.get(id)






