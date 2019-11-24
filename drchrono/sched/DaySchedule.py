from social_django.models import UserSocialAuth
import datetime
import drchrono.dates as dates

from drchrono.endpoints import  AppointmentEndpoint, PatientEndpoint

class DaySchedule:

    def __init__ (self, doctor_id):
        self.__access_tok = self.__get_token()
        self.__doc_id = doctor_id

    def __get_token(self):
        """
        Social Auth module is configured to store our access tokens. This dark magic will fetch it for us if we've
        already signed in.
        """
        oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
        access_token = oauth_provider.extra_data['access_token']
        return access_token


    def get_appointments (self, date):
        api = AppointmentEndpoint(self.__access_tok)
        today_ymd = date.strftime('%Y-%m-%d')
        all = api.list(params={'doctor': self.__doc_id}, date=today_ymd)
        return all

    def get_todays_appointments (self):
        return sorted(self.get_appointments(datetime.date.today()), key=lambda a: a['scheduled_time'])

    def get_patient (self, patient_id):
        api = PatientEndpoint(self.__access_tok)
        return api.fetch(patient_id)

    def get_patient_appointments (self):
        appointments = self.get_todays_appointments()
        appt_list = []
        for a in appointments:
            patient_id = a['patient']
            p = self.get_patient(patient_id)
            scheduled_time = dates.time_format(a['scheduled_time'])
            appt_list.append({'first_name': p['first_name'], 'last_name': p['last_name'], 'reason': a['reason'],
                              'scheduled_time': scheduled_time})
        return appt_list
