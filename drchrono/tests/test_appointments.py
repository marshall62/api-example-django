import pytest
import datetime
import drchrono.dates as dateutil
from drchrono.endpoints import DoctorEndpoint
from drchrono.models.Doctor import Doctor
from drchrono.models.Patient import Patient
from drchrono.models.Appointment import Appointment
from drchrono.models.Appointments import Appointments
from drchrono.models.PatientAppointment import PatientAppointment
from .api_access import get_access_tok


def test_doc_endpoint ():
    access_tok = get_access_tok()
    ep = DoctorEndpoint(access_tok)
    d = next(ep.list())
    assert d != None


def test_doc_obj ():
    d = Doctor()
    assert d != None
    assert d.last_name == 'Marshall'


def test_patient ():
    p = Patient(fname='Jenny', lname='Harris')
    assert p != None
    id = p.id
    p = Patient(id=id)
    assert p != None
    assert p.last_name == 'Harris' and p.first_name == 'Jenny'
    p = Patient(data=p.data)
    assert p.last_name == 'Harris' and p.first_name == 'Jenny'
    assert p.id == id
    p = Patient()
    assert p.data == {} and p.id == None

def test_appointments ():
    doc = Doctor()
    appts = Appointments(doc)
    all = appts.get_appointments_for_date()
    for a in all:
        assert type(a) is PatientAppointment

    p = Patient(fname='Jenny', lname='Harris')
    all = appts.get_appointments_for_patient(p.id)
    for a in all:
        assert a.patient_id == p.id

def test_create_apppointment ():
    doc = Doctor()
    p = Patient(fname='Jenny', lname='Harris')
    a = Appointment(doctor=doc) # new empty appointment
    # TODO new appointment must have all required fields.  Need to set reasonable defaults when create.

    a.patient_id = p.id
    tz = datetime.tzinfo.utcoffset(5)
    ts = datetime.datetime.now(tz) # timezone is wrong by 5 hours.   TODO correct
    a.scheduled_time = dateutil.timestamp_api_format(ts)
    json = a.create() # save to API
    print("json of new appt is", json)
    assert(json != None)

def test_appointment_status_chg ():
    ''' poorly done:  it tests setting status of a appointment persist to API.  Does
    this by changing appointments to "Arrived" and then changing them back.  If it fails,
    the appointment might be left in "Arrived" setting. '''
    doc = Doctor()
    appts = Appointments(doc)
    p = Patient(fname='Jenny', lname='Harris')
    all = appts.get_appointments_for_patient(p.id)
    orig_statuses = {}
    for a in all:
        appt_id = a.appointment_id
        stat = a.status
        orig_statuses[appt_id] = stat # save the original status
        a.status = 'Arrived' # will persist it to API
    all = appts.get_appointments_for_patient(p.id)
    for a in all:
        stat = a.status
        assert stat == 'Arrived'
        a.status = orig_statuses[a.appointment_id] # set it back to the original






