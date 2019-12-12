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






