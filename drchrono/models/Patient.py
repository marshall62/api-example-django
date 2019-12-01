from drchrono.endpoints import PatientEndpoint
from drchrono.models.APIObj import APIObj


class Patient(APIObj):

    def __init__(self, data={}, id=None, fname=None, lname=None, ssn4=None):
        if data:
            super().__init__(data=data, endpoint=PatientEndpoint)
        elif id != None:
            super().__init__(endpoint=PatientEndpoint)
            self.load_by_id(id)
        elif fname and lname and ssn4:
            super().__init__(endpoint=PatientEndpoint)
            self._load_by_name(fname,lname, ssn4)
        else:
            super().__init__(endpoint=PatientEndpoint)


    def _load_by_name(self, fname, lname, ssn4):
        patients = self._endpoint.list(first_name=fname, last_name=lname, ssn4=ssn4)
        if len(patients) == 1:
            self._data = patients[0] if patients else None


    @property
    def first_name (self):
        return self._data['first_name']

    @property
    def last_name (self):
        return self._data['last_name']

    @property
    def ssn4 (self):
        return self._data['social_security_number'][-4:]


    def __repr__ (self):
        return "<Patient {} {} {}>".format(self.first_name, self.last_name, self.ssn4)

