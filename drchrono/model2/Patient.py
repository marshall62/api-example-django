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
    def gender (self):
        return self._data['gender']

    @property
    def nick_name (self):
        return self._data['nick_name']

    @property
    def last_name (self):
        return self._data['last_name']

    @property
    def ssn4 (self):
        return self._data['social_security_number'][-4:]

    @property
    def data (self):
        return self._data

    def modify (self, data):
        '''
        merge the given data into the existing data dict
        '''
        self._data.update(data)


    def __repr__ (self):
        return "<Patient {} {} {}>".format(self.first_name, self.last_name, self.ssn4)

