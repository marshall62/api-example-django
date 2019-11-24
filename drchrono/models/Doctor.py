from drchrono.endpoints import DoctorEndpoint
from drchrono.models.APIObj import APIObj


class Doctor(APIObj):

    def __init__(self):
        super().__init__()
        self.__doc = self.__get_doc()
        self.__doc_id = self.__doc['id']

    @property
    def obj (self):
        return self.__doc

    @property
    def id (self):
        return self.__doc_id

    def __get_doc(self):
        """
        Return the current doctor
        """
        api = DoctorEndpoint(self._access_tok)
        # Grab the first doctor from the list; normally this would be the whole practice group, but your hackathon
        # account probably only has one doctor in it.
        return next(api.list())
