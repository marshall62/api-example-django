from drchrono.api_models.Appointment import Appointment, APIObj
from drchrono.endp.EndpointMgr import EndpointMgr
from drchrono.api_models.Patient import Patient
import drchrono.models
import drchrono.api_models.PatientAppointment as api
import drchrono.dates as dateutil
import datetime

from drchrono.sched.ApptMgr import ApptMgr
import drchrono.model2.Patient as m2Patient
import drchrono.model2.Appointment as m2Appointment


class Appointments():

    _doctor = None


    @classmethod
    def set_doctor (cls, doctor):
        cls._doctor = doctor


    @classmethod
    def get_appointments_for_date (cls, date=datetime.date.today(), patient_id=None):
        '''
        gets all the appointments for the date regardless of status
        :return: List[PatientAppointment] objects for today
        '''
        today_ymd = date.strftime('%Y-%m-%d')
        params = {'doctor': cls._doctor.id}
        if patient_id:
            params['patient'] = patient_id
        endpoint = EndpointMgr.appointment()(APIObj.get_token())
        today_appts = endpoint.list(params=params, verbose=True, date=today_ymd)
        result = [] #type: List[api.PatientAppointment]
        count = 0
        for a in today_appts:
            appt = Appointment(data=a)
            pat = Patient(id=appt.patient_id)
            pa = api.PatientAppointment(patient=pat, appointment=appt)
            count += 1
            result.append(pa)
        return sorted(result, key=lambda pa: pa.scheduled_time)

    @staticmethod
    def is_active (appt):
        return appt.status not in ['Complete', 'Cancelled']

    @classmethod
    def get_active_appointments_for_date (cls, date=datetime.date.today(), patient_id=None):
        '''
        gets all the appointments for the date leaving out canceled and complete ones.
        :return: List[PatientAppointment] objects for today sorted by scheduled time
        '''
        today_ymd = date.strftime('%Y-%m-%d')
        params = {'doctor': cls._doctor.id}
        if patient_id:
            params['patient'] = patient_id
        endpoint = EndpointMgr.appointment()(APIObj.get_token())
        today_appts = endpoint.list(params=params, verbose=True, date=today_ymd)
        result = [] #type: List[api.PatientAppointment]
        count = 0
        for a in today_appts:
            appt = Appointment(data=a)
            if cls.is_active(appt):
                pat = Patient(id=appt.patient_id)
                pa = api.PatientAppointment(patient=pat, appointment=appt)
                count += 1
                result.append(pa)
        return sorted(result, key=lambda pa: pa.scheduled_time)





    @classmethod
    def get_appointments_for_patient (cls, patient_id, date=datetime.date.today()):
        return cls.get_appointments_for_date(date=date, patient_id=patient_id)

    @staticmethod
    def make_appointment_for_patient (patient, date=datetime.date.today(), duration=15, reason=''):
        appt = Appointment.create(patient.id,scheduled_time=dateutil.timestamp_api_format(date), duration=duration, reason=reason)
        pa = api.PatientAppointment(patient=patient, appointment=appt)
        return pa


    #  Not using any local database stuff.  Can delete once I'm confident I don't want
    @classmethod
    def load_all_appointments (cls):
        patient_appts = cls.get_active_appointments_for_date()
        for pa in drchrono.models.PatientAppointment.objects.all():
            pa.delete()
        for a in patient_appts:
            pa = drchrono.models.PatientAppointment(first_name=a.first_name, last_name=a.last_name, patient_id=a.patient_id,
                                          appointment_id=a.appointment_id, ssn4=a.ssn4, reason=a.reason,
                                          scheduled_time=dateutil.apidt_to_ts(a.scheduled_time), status=a.status,
                                          expected_duration=a.duration)
            pa.save()

