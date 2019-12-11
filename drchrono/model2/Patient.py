class Patient:


    def __init__(self, data):
        self._data = data

    @property
    def id (self):
        return self._data['id']

    @property
    def first_name (self):
        return self._data['first_name']

    @property
    def last_name (self):
        return self._data['last_name']

    @property
    def ssn4 (self):
        return self._data['social_security_number'][-4:]

    @property
    def data (self):
        return self._data


    def __repr__ (self):
        return "<Patient {} {} {}>".format(self.first_name, self.last_name, self.ssn4)

