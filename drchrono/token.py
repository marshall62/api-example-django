from drchrono.tests.api_access import get_access_tok
from social_django.models import UserSocialAuth

import os

def get_token():
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