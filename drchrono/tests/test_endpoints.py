from drchrono.endp.endpoints import AppointmentEndpoint, DoctorEndpoint, PatientSummaryEndpoint
from drchrono.apitoken import get_token


def test_appt ():
    ep = DoctorEndpoint(get_token())
    doc = next(ep.list())
    ep = AppointmentEndpoint(get_token())

    all = ep.list(date='2019-12-12')
    for a in all:
        print(a)
    assert len(all) > 0

def test_patient_list ():
    ep = DoctorEndpoint(get_token())
    doc = next(ep.list())
    drid = doc['id']
    ep = PatientSummaryEndpoint(get_token())
    all = ep.list(doctor_id=drid)
    assert len(all) > 0

def test_pt_upd ():
    ep = DoctorEndpoint(get_token())
    doc = next(ep.list())
    drid = doc['id']
    ep = PatientSummaryEndpoint(get_token())
    all = ep.list(doctor_id=drid)
    p1 = all[0]
    print('update of ', p1)
    ep.update(id=p1['id'],data={'first_name': 'Phred'}, partial=True)
    p = ep.fetch(id=p1['id'])
    assert p['first_name'] == 'Phred'



