from drchrono.endpoints import PatientEndpoint
from drchrono.models.APIObj import APIObj


class Patient(APIObj):

    def __init__(self):
        super().__init__()


    @property
    def obj (self):
        return self.__doc

    @property
    def id (self):
        return self.__doc_id

    def get_patient(self, fname, lname, ssn4):
        """
        Return the current doctor
        """
        api = PatientEndpoint(self._access_tok)
        patients = api.list(first_name=fname, last_name=lname, ssn4=ssn4)
        # there should be only one with this ssn so return first
        return patients[0] if patients else None
