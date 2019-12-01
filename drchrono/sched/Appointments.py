from drchrono.endpoints import AppointmentEndpoint
from drchrono.models.APIObj import APIObj
from drchrono.models.Appointment import Appointment
from drchrono.models.Patient import Patient
from drchrono.models.PatientAppointment import PatientAppointment
import datetime


class Appointments(APIObj):
    '''
    Methods to fetch appointments from the API
    '''
    def __init__(self, doctor):
        super().__init__(endpoint=AppointmentEndpoint)
        self._doctor = doctor #type: Doctor

    def get_appointments_for_date (self, date=datetime.date.today(), patient_id=None):
        '''
        :return: List[PatientAppointment] objects for today
        '''
        today_ymd = date.strftime('%Y-%m-%d')
        params = {'doctor': self._doctor.id}
        if patient_id:
            params['patient'] = patient_id
        today_appts = self._endpoint.list(params=params, date=today_ymd)
        result = [] #type: List[PatientAppointment]
        count = 0
        for a in today_appts:
            appt = Appointment(data=a)
            pat = Patient(id=appt.patient_id)
            pa = PatientAppointment(patient=pat, appointment=appt)
            count += 1
            result.append(pa)
        return result

    def get_appointments_for_patient (self, patient_id, date=datetime.date.today()):
        return self.get_appointments_for_date(date=date, patient_id=patient_id)





