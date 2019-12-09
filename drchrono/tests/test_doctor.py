from drchrono.api_models.Doctor import Doctor
from drchrono.endp.endpoints import DoctorEndpoint, OfficeEndpoint
from .api_access import get_access_tok

class TestDoctor:


    def test_doc_endpoint (self):
        access_tok = get_access_tok()
        ep = DoctorEndpoint(access_tok)
        docs = list(ep.list())
        assert 1 == len(docs)
        d = next(ep.list())
        assert d != None

    def test_office_endpoint (self):
        access_tok = get_access_tok()
        ep = DoctorEndpoint(access_tok)
        doc = next(ep.list())
        ep = OfficeEndpoint(access_tok)
        all_offices = list(ep.list())
        found = []
        for o in all_offices:
            if o['doctor'] == doc['id']:
                found.append(o)

        assert 1 == len(found)



    def test_doc_obj (self):
        d = Doctor()
        assert d != None
        assert d.last_name == 'Marshall'


    def test_doc_patients (self):
        d = Doctor()
        patients = d.get_patients()
        assert 0 < len(patients)


