from drchrono.sched.PatientMgr import PatientMgr
from drchrono.sched.ModelObjects import ModelObjects
from drchrono.sched.APIGateway import APIGateway


def test_patient__by_name ():
    '''test a failed lookup'''

    pats = PatientMgr.get_patients_from_name("dennis","martineXXX")
    assert [] == pats

    pats = PatientMgr.get_patients_from_name("Peter","Django", "0000")
    assert [] == pats

    pats = PatientMgr.get_patients_from_name("Eva","Genmark")
    assert 1 <= len(pats)

    pats = PatientMgr.get_patients_from_name("dennis", "martin")
    assert 1 < len(pats)




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

def test_patient_upd_summary ():
    pats = PatientMgr.get_patients_from_name("Eva","Genmark")
    p1 = pats[0]
    gen = p1.gender
    mods = {'gender': 'Male'}
    p1.modify(mods)
    PatientMgr.update_patient(p1) # write to API patient summary
    # need to reload from data store
    ModelObjects().reload_patients()
    pats = PatientMgr.get_patients_from_name("Eva", "Genmark")
    p1 = pats[0]
    assert p1.gender == 'Male'
    mods = {'gender': gen}
    p1.modify(mods)
    PatientMgr.update_patient(p1)  # restore original gender to api

def test_patient_upd ():
    pats = PatientMgr.get_patients_from_name("Eva","Genmark")
    p1 = pats[0]
    mods = {'nick_name': 'Ev'}
    # mods must be included to Patient endpoint to be used as partials.
    PatientMgr.update_patient(p1, new_data=mods, summary=False) # write to API patient
    # need to reload from data store
    ModelObjects().reload_patients()
    pats = PatientMgr.get_patients_from_name("Eva", "Genmark")
    p1 = pats[0]
    assert p1.nick_name == 'Ev'



