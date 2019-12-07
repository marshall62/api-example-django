from drchrono.api_models.Doctor import Doctor
from drchrono.endpoints import DoctorEndpoint
from .api_access import get_access_tok

class TestDoctor:

    def setup_class(cls):
        cls.doctor = Doctor()


    def test_doc_endpoint (self):
        access_tok = get_access_tok()
        ep = DoctorEndpoint(access_tok)
        d = next(ep.list())
        assert d != None


    def test_doc_obj (self):
        d = Doctor()
        assert d != None
        assert d.last_name == 'Marshall'


    def test_doc_patients (self):
        patients = self.doctor.get_patients()
        assert 0 < len(patients)


