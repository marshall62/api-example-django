from drchrono.endpoints import AppointmentEndpoint
from drchrono.api_models.APIObj import APIObj
from drchrono.api_models.Doctor import Doctor
from drchrono.api_models.Appointment import Appointment
from drchrono.api_models.Patient import Patient
import drchrono.models
import drchrono.api_models.PatientAppointment as api
import drchrono.dates as dateutil
import datetime


class Appointments(APIObj):
    '''
    Methods to fetch appointments from the API
    '''
    def __init__(self, doctor=None):
        super().__init__(endpoint=AppointmentEndpoint)
        self._doctor = doctor if doctor else Doctor()


    def get_appointments_for_date (self, date=datetime.date.today(), patient_id=None):
        '''
        gets all the appointments for the date regardless of status
        :return: List[PatientAppointment] objects for today
        '''
        today_ymd = date.strftime('%Y-%m-%d')
        params = {'doctor': self._doctor.id}
        if patient_id:
            params['patient'] = patient_id
        today_appts = self._endpoint.list(params=params, date=today_ymd)
        result = [] #type: List[api.PatientAppointment]
        count = 0
        for a in today_appts:
            appt = Appointment(data=a)
            pat = Patient(id=appt.patient_id)
            pa = api.PatientAppointment(patient=pat, appointment=appt)
            count += 1
            result.append(pa)
        return result

    @staticmethod
    def is_active (appt):
        return appt.status not in ['Complete', 'Cancelled']

    def get_active_appointments_for_date (self, date=datetime.date.today(), patient_id=None):
        '''
        gets all the appointments for the date leaving out canceled and complete ones.
        :return: List[PatientAppointment] objects for today
        '''
        today_ymd = date.strftime('%Y-%m-%d')
        params = {'doctor': self._doctor.id}
        if patient_id:
            params['patient'] = patient_id
        today_appts = self._endpoint.list(params=params, date=today_ymd)
        result = [] #type: List[api.PatientAppointment]
        count = 0
        for a in today_appts:
            appt = Appointment(data=a)
            if self.is_active(appt):
                pat = Patient(id=appt.patient_id)
                pa = api.PatientAppointment(patient=pat, appointment=appt)
                count += 1
                result.append(pa)
        return result

    def get_appointments_for_patient (self, patient_id, date=datetime.date.today()):
        return self.get_appointments_for_date(date=date, patient_id=patient_id)



    def load_all_appointments (self):
        patient_appts = self.get_active_appointments_for_date()
        for pa in drchrono.models.PatientAppointment.objects.all():
            pa.delete()
        for a in patient_appts:
            pa = drchrono.models.PatientAppointment(first_name=a.first_name, last_name=a.last_name, patient_id=a.patient_id,
                                          appointment_id=a.appointment_id, ssn4=a.ssn4, reason=a.reason,
                                          scheduled_time=dateutil.apidt_to_ts(a.scheduled_time), status=a.status,
                                          expected_duration=a.duration)
            pa.save()

