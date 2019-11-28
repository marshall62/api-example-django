from social_django.models import UserSocialAuth
from drchrono.tests.api_access import get_access_tok
import os

class APIObj:

    def __init__ (self, data={}, endpoint=None):
        self._access_tok = self._get_token()
        self._endpoint = endpoint(self._access_tok)
        self._data = data
        self._id = data['id'] if data else None

    @property
    def id (self):
        return self._id

    @property
    def data (self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data
        self._id = data['id']

    def update (self):
        '''
        Persist the full data to the API (regardless of whether changed)
        :return:
        '''
        self._endpoint.update(id=self.id, data=self.data, partial=False)

    def create (self):
        '''
        Write the object to the API and return the data
        :return:
        '''
        json = self._endpoint.create(data=self.data)
        return json

    def _data_update_persist (self, property, value):
        '''
        Change a property on an API object.  This will change it via the API.
        :param property:
        :param value:
        :return:
        '''
        # if the new value is different than the current value change it and persist to API
        if value != self.data[property]:
            self.data[property] = value
            self._endpoint.update(id=self.id, data={property: value})

    def load_by_id (self, id):
        self._id = id
        self._data = self._endpoint.fetch(id=id)
        return self._data

    def _get_token(self):
        """
        Social Auth module is configured to store our access tokens. This dark magic will fetch it for us if we've
        already signed in.
        """
        if os.environ.get('UNIT_TESTING'):
           return get_access_tok()
        else:
            oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
            access_token = oauth_provider.extra_data['access_token']
            return access_token