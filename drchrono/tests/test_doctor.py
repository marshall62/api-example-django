from drchrono.api_models.Doctor import Doctor
from drchrono.sched.Patients import Patients
from drchrono.endpoints import DoctorEndpoint
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


def test_doc_patients ():
    d = Doctor()
    pf = Patients(d)
    assert len(pf.patients) > 0

