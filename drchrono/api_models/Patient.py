from drchrono.endp.endpoints import PatientEndpoint
from drchrono.endp.EndpointMgr import EndpointMgr
from drchrono.api_models.APIObj import APIObj
from drchrono.exc.exceptions import NonUniqueException, NotFoundException


class Patient(APIObj):



    def __init__(self, data={}, id=None, first_name=None, last_name=None, ssn4=None):
        if data:
            super().__init__(data=data, endpoint=EndpointMgr.patient())
        elif id != None:
            super().__init__(endpoint=EndpointMgr.patient())
            self.load_by_id(id)
        elif first_name and last_name:
            super().__init__(endpoint=EndpointMgr.patient())
            self._load_by_name(first_name, last_name, ssn4)
        else:
            super().__init__(endpoint=EndpointMgr.patient())


    @staticmethod
    def create (first_name, last_name, social_security_number, gender, doctor):
        return APIObj._create({'first_name':first_name,
                               'last_name':last_name,
                               'social_security_number':social_security_number,
                               'gender':gender,
                                'doctor': doctor}, Patient, PatientEndpoint)



    def _load_by_name(self, fname, lname, ssn4):
        patients = self._endpoint.list(first_name=fname, last_name=lname, ssn4=ssn4)
        if len(patients) == 1:
            self._data = patients[0] if patients else None
        elif len(patients) > 1:
            raise NonUniqueException("Could not find a single patient with that name.  Please use SSN")
        else:
            raise NotFoundException("Patient could not be found")



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

