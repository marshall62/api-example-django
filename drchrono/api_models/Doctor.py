from drchrono.endpoints import DoctorEndpoint, OfficeEndpoint
from drchrono.api_models.APIObj import APIObj


class Doctor(APIObj):
    ''' Singleton Doctor loaded from API only once'''
    instance = None


    def __init__ (self):
        if not Doctor.instance:
            Doctor.instance = Doctor.__Doctor()


    class __Doctor(APIObj):
        def __init__(self):
            super().__init__(endpoint=DoctorEndpoint)
            self._data = self._get_data()
            self._id = self._data['id']
            self._set_office()

        def _set_office (self):
            office_api = OfficeEndpoint(self._access_tok)
            office = next(office_api.list(data={'doctor': self.id}))  # there better only be one
            self._data['office'] = office['id']

        def _get_data(self):
            return next(self._endpoint.list())

    @property
    def id (self):
        return Doctor.instance.id

    @property
    def data (self):
        return Doctor.instance.data

    @property
    def first_name (self):
        return Doctor.instance._data['first_name']

    @property
    def last_name (self):
        return Doctor.instance._data['last_name']
