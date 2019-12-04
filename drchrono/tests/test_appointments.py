import pytest
import datetime
from itertools import cycle
from .api_access import get_access_tok
from drchrono.api_models.Doctor import Doctor
from drchrono.api_models.Appointment import Appointment
from drchrono.sched.Appointments import Appointments
from drchrono.sched.Patients import Patients
from drchrono.api_models.PatientAppointment import PatientAppointment
from drchrono.endpoints import AppointmentEndpoint
import drchrono.dates as dateutil
import random


class TestAppointments:

    def setup_class(cls):
        cls.doctor = Doctor()
        cls.pf = Patients(cls.doctor)
        cls.patients = cls.pf.patients
        cls.patient1 = cls.patients[0]


    def test_get_all_appts (self):
        pa_list = Appointments().get_appointments_for_date()
        for pa in pa_list:
            a = pa.appointment
            assert None != a.status_transitions # status change history (useful)
            print(pa)
        print (len(pa_list))
        assert len(pa_list) > 0

    def test_set_all_appts_status (self):
        '''
        Put some reasonable statuses on todays appointments.
        :return:
        '''
        pa_list = Appointments().get_appointments_for_date()
        for pa in pa_list:
            v = random.random()
            if v < 0.1:
                pa.status = 'In Session'
            elif v < 0.4:
                pa.status = 'Checked In'
            else:
                pa.status = ''

        pa_list = Appointments().get_appointments_for_date()
        for pa in pa_list:
            print(pa)

        assert len(pa_list) > 0


    @pytest.mark.skip
    def test_appointments (self):
        af = Appointments(TestAppointments.doctor)
        all = af.get_appointments_for_date()
        for a in all:
            assert type(a) is PatientAppointment

        p = TestAppointments.patient1
        all = af.get_appointments_for_patient(p.id)
        for a in all:
            assert a.patient_id == p.id


    @pytest.mark.skip
    def test_appt_status_chg (self):
        ''' change the status of the first patients first appointment to No Show'''
        p = TestAppointments.patient1
        a = Appointments(TestAppointments.doctor)
        appts = a.get_appointments_for_patient(patient_id=p.id)
        if len(appts) > 0:
            a1 = appts[0]
            id = a1.appointment_id
            status1 = a1.status
            a1.status = 'No Show' # updates this appt status with API
            appts = a.get_appointments_for_patient(patient_id=p.id)
            a1 = appts[0]
            assert id == a1.appointment_id
            assert 'No Show' == a1.status
            a1.status = status1 # restore to the original status (not verifying it succeeds)


    @pytest.mark.skip
    def test_create_apppointment (self):
        '''
        Create an appointment (time= now ) for patient 1
        :return:
        '''
        p = TestAppointments.patient1
        a = Appointment(doctor=TestAppointments.doctor) # new empty appointment

        a.patient_id = p.id

        ts = datetime.datetime.now()
        a.scheduled_time = dateutil.timestamp_api_format(ts)
        json = a.create() # save to API
        print("json of new appt is", json)
        assert(json != None)
        created_appt_id = json['id']
        appts = Appointments(TestAppointments.doctor)
        patient_appointments = appts.get_appointments_for_patient(patient_id=p.id)
        found = False
        for pa in patient_appointments:
            if pa.appointment.id == created_appt_id:
                found = True
        assert found, "Created appointment was not found when looking up patients appointments"

    @pytest.mark.skip
    def test_create_N_appointments (self):
        '''
        Create N appointments at random times today for different patients
        Will use this to test UI.
        :return:
        '''
        patients = TestAppointments.patients
        N = 20
        count = 0
        ts = datetime.datetime.now()
        appointment_ids = []
        for p in cycle(patients):
            # add 30 minutes to timestamp for each new appointment
            a = Appointment(doctor=TestAppointments.doctor, data={})
            ts = ts + datetime.timedelta(minutes=30)
            a.scheduled_time = dateutil.timestamp_api_format(ts)
            a.patient_id = p.id
            json = a.create() # save to API
            print(json)
            appointment_ids.append(json['id'])
            count += 1
            if count >= N:
                break

        assert 10 == len(appointment_ids)


    @pytest.mark.skip
    def test_appointment_status_empty (self):

        appts = Appointments(TestAppointments.doctor)
        p = TestAppointments.patient1
        all = appts.get_appointments_for_patient(p.id)
        orig_statuses = {}
        for a in all:
            appt_id = a.appointment_id
            stat = a.status
            orig_statuses[appt_id] = stat # save the original status
            a.status = '' # will persist it to API
        all = appts.get_appointments_for_patient(p.id)
        for a in all:
            stat = a.status
            assert '' == stat









