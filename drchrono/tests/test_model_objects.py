from drchrono.sched.AppointmentMgr import AppointmentMgr
from drchrono.sched.ModelObjects import ModelObjects
from drchrono.datastore.APIGateway import APIGateway
from drchrono.model2.Doctor import Doctor
import pytest
import pickle




@pytest.mark.django_db
def test_singl ():
    mf = ModelObjects()
    mf2 = ModelObjects()
    assert mf == mf2
    assert mf is mf2

@pytest.mark.django_db
def test_map_pat ():
    ModelObjects.instance = None
    mf = ModelObjects(load_local=False)
    for k in mf.patients_map.keys():
        assert 0 < k

@pytest.mark.django_db
def test_map_apt ():
    ModelObjects.instance = None
    mf = ModelObjects(load_local=False)
    for k in mf.appointments_map.keys():
        assert 0 < k


@pytest.mark.django_db
def test_map_pat_db ():
    ModelObjects.instance = None
    mf = ModelObjects(load_local=True)
    for k in mf.patients_map.keys():
        assert 0 < k

@pytest.mark.django_db
def test_map_apt_db ():
    mf = ModelObjects(load_local=True)
    for k in mf.appointments_map.keys():
        assert 0 < k


@pytest.mark.django_db
def test_api_model ():
    ModelObjects.instance = None
    m = ModelObjects(load_local=True)
    pats_api = m.patients
    apts_api = m.appointments
    assert len(pats_api) > 0
    assert len(apts_api) > 0
    db = m.local_db
    pats_db = db._patients
    apts_db = db._appointments

    assert len(pats_db) > 0
    assert len(apts_db) > 0
    assert len(pats_db) == len(pats_api)
    assert len(apts_db) == len(apts_api)
    print("patients in db")
    for p in pats_db:
        print(pickle.loads(p.data))
    print("appointments in db")
    for a in apts_db:
        print(pickle.loads(a.data))

@pytest.mark.django_db
def test_dr ():
    ModelObjects.instance = None
    mf = ModelObjects(load_local=False)
    doc = mf.doctor
    assert doc != None
    assert type(doc) == Doctor

@pytest.mark.django_db
def test_appts ():
    ModelObjects.instance = None
    mf = ModelObjects(load_local=False)
    appointments = mf.appointments
    assert type(appointments) == list
    for a in appointments:
        print(a)

@pytest.mark.django_db
def test_patients ():
    ModelObjects.instance = None
    mf = ModelObjects(load_local=False)
    pats = mf.patients
    assert type(pats) == list
    for p in pats:
        print(p)

@pytest.mark.django_db
def test_dr_patient_appts ():
    ModelObjects.instance = None
    d = ModelObjects(load_local=False).doctor
    pas = d.get_patient_appointments()
    assert type(pas) == list
    for p in pas:
        print(p)

@pytest.mark.django_db
def test_appointment_property_chg ():
    '''
    Complex test to verify that APIGateway structures are shared correctly with the ModelObject
    which supports a simple change to the ModelObject being reflected in the APIGateway structure
    :return:
    '''
    # create a new appointment record
    id = -22
    apt_rec = {'id':id, 'status': 'Phred'}
    # add to the gateway
    gw = APIGateway()
    gw.appointments.append(apt_rec)
    gw.appointments_map[id] = apt_rec
    # now reset the ModelObjects
    ModelObjects.instance = None
    # creates a new ModelObjects loaded from the gw
    m = ModelObjects(load_local=False)

    # verify all structures are correctly shared

    # verify model has Appointments that are correct
    apt_from_map = m.appointments_map[id]
    apt_from_list = [a for a in m.appointments if a.id == id][0]
    assert apt_from_map == apt_from_list
    assert apt_from_map is apt_from_list

    #verify that gw holds data that is same as these objects
    gw_rec1 = gw.appointments_map[id]
    gw_rec2 = [r for r in gw.appointments if r['id'] == id][0]
    assert gw_rec1 == gw_rec2
    assert gw_rec1 is gw_rec2
    assert gw_rec1 == apt_from_map.data

    # verify a status change in this appointment is reflected throughout

    apt = m.appointments_map[id]
    newstat = 'BLEK'
    apt.status=newstat
    rec = gw.appointments_map[id]
    assert rec['status'] == newstat
    a1 = m.appointments_map[id]
    assert a1.status == newstat

    # verify model method for status change works similary
    AppointmentMgr.set_appointment_status(id, 'PHRED', persist=False)
    assert a1.status == 'PHRED'


