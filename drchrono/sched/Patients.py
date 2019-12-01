from drchrono.endpoints import PatientEndpoint
from drchrono.models.APIObj import APIObj
from drchrono.models.Patient import Patient

class Patients(APIObj):

    def __init__(self, doctor):
        super().__init__(endpoint=PatientEndpoint)
        self._doctor = doctor #type: Doctor
        self._patients = self._get_patients()

    @property
    def patients (self):
        return self._patients

    def _get_patients (self):
        '''
        Get all the patients who have this doctor
        :return:
        '''
        pats = self._endpoint.list(params={'doctor': self._doctor.id})
        result = []
        for p in pats:
            x = Patient(data=p)
            result.append(x)

        return result

    def get_patient1 (self):
        '''
        Get the first patient found for this doctor (for testing only)
        :return:
        '''
        pats = self._endpoint.list(params={'doctor': self._doctor.id})
        return Patient(data=pats[0])