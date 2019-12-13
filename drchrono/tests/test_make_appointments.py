from drchrono.sched.ModelObjects import ModelObjects
from drchrono.model2.Appointment import Appointment
from drchrono.sched.AppointmentMgr import AppointmentMgr
from drchrono.model2.Doctor import Doctor
import pytest
import datetime
import drchrono.dates as dateutil
from itertools import cycle
import random

def make_appointment_for_patient (p, ts):
    m = ModelObjects()
    doc = m.doctor
    apt = Appointment({'patient':p.id, 'duration': 30, 'reason': 'Feeling sick', 'exam_room': 1,
                       'office': doc.office, 'doctor': doc.id,
                       'scheduled_time': dateutil.timestamp_api_format(ts)})
    apt = AppointmentMgr.save_appointment(apt)
    return apt

# @pytest.mark.skip
def test_make_1_appt ():
    m = ModelObjects()
    p1 = m.patients[0]
    ts = datetime.datetime.now() + datetime.timedelta(minutes=30)
    apt = make_appointment_for_patient(p1,ts)
    print(apt)
    assert apt.patient_id == p1.id

@pytest.mark.skip
def test_make_1_appt_before_now ():
    m = ModelObjects()
    p1 = m.patients[8]
    ts = datetime.datetime.now() - datetime.timedelta(minutes=200)
    apt = make_appointment_for_patient(p1,ts)
    print(apt)
    assert apt.patient_id == p1.id

@pytest.mark.skip
def test_make_1_random_appt ():
    m = ModelObjects()
    p1 = random.choice(m.patients)
    minutes = random.randint(0,8)*30
    ts = datetime.datetime.now() + datetime.timedelta(minutes=minutes)
    apt = make_appointment_for_patient(p1,ts)
    print(apt)
    assert apt.patient_id == p1.id

@pytest.mark.skip
def test_create_N_appointments ():
    '''
    Create N appointments at random times today for different patients
    Will use this to test UI.
    :return:
    '''
    m = ModelObjects()
    patients = m.patients
    N = 20
    count = 0
    ts = datetime.datetime.now()
    appointments = []
    for p in cycle(patients):
        # add 30 minutes to timestamp for each new appointment
        ts = ts + datetime.timedelta(minutes=30)
        # dennis martin was created in API for test but I can't delete.  Don't want appts for him.
        if p.first_name == 'dennis' and p.last_name=='martin':
            continue
            #patient.id,scheduled_time=dateutil.timestamp_api_format(date), duration=duration, reason=reason)
        appointments.append(make_appointment_for_patient(p,ts))
        count += 1
        if count == N:
            break
    m.reload_appointments()
    assert N == len(appointments)