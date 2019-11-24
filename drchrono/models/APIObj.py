from social_django.models import UserSocialAuth

class APIObj:

    def __init__ (self):
        self._access_tok = self.__get_token()

    def __get_token(self):
        """
        Social Auth module is configured to store our access tokens. This dark magic will fetch it for us if we've
        already signed in.
        """
        oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
        access_token = oauth_provider.extra_data['access_token']
        return access_token