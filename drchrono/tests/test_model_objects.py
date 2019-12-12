from drchrono.sched.AppointmentMgr import AppointmentMgr
from drchrono.sched.PatientMgr import PatientMgr
from drchrono.sched.ModelObjects import ModelObjects
from drchrono.sched.APIGateway import APIGateway
from drchrono.model2.Doctor import Doctor
from drchrono.model2.Appointment import Appointment


def test_singl ():
    mf = ModelObjects()
    mf2 = ModelObjects()
    assert mf == mf2
    assert mf is mf2


def test_dr ():
    mf = ModelObjects()
    doc = mf.doctor
    assert doc != None
    assert type(doc) == Doctor


def test_appts ():
    mf = ModelObjects()
    appointments = mf.appointments
    assert type(appointments) == list
    for a in appointments:
        print(a)

def test_patients ():
    mf = ModelObjects()
    pats = mf.patients
    assert type(pats) == list
    for p in pats:
        print(p)

def test_dr_patient_appts ():
    d = ModelObjects().doctor
    pas = d.get_patient_appointments()
    assert type(pas) == list
    for p in pas:
        print(p)

def test_patient__by_name ():
    '''test a failed lookup'''

    m = ModelObjects()
    pats = PatientMgr.get_patients_from_name("dennis","martineXXX")
    assert [] == pats

    pats = PatientMgr.get_patients_from_name("Peter","Django", "0000")
    assert [] == pats

    # There are two Peter Djangos
    pats = PatientMgr.get_patients_from_name("Peter","Django")
    assert 1 < len(pats)

    # this lookup should succeed because we include ssn to uniquely id.
    pats = PatientMgr.get_patients_from_name("Peter","Django","8888")
    assert 1 == len(pats)
    assert 'Django' == pats[0].last_name



def test_patient_by_id ():

    m = ModelObjects()
    pat1 = m.patients[0]
    assert pat1 != None
    pp = PatientMgr.get_patient_by_id(pat1.id)
    print(id(pat1), id(pp))
    # verify they are same.
    assert pp == pat1

    pp = PatientMgr.get_patient_by_id(-34)
    assert None == pp

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
    m = ModelObjects()

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



