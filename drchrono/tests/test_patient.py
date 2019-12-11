import pytest
from drchrono.api_models.Patient import Patient
from drchrono.api_models.Doctor import Doctor
from drchrono.exc.exceptions import NotFoundException, NonUniqueException
from drchrono.sched.ModelObjects import ModelObjects

class TestPatient:

    def setup_class(cls):
        cls.m = ModelObjects()

    def teardown_class (cls):
        pass




    def test_patient__by_name (self):
        '''test a failed lookup'''

        m = ModelObjects()
        pats = m.get_patients_from_name("dennis","martineXXX")
        assert [] == pats

        pats = m.get_patients_from_name("Peter","Django", "0000")
        assert [] == pats

        # There are two Peter Djangos
        pats = m.get_patients_from_name("Peter","Django")
        assert 1 < len(pats)

        # this lookup should succeed because we include ssn to uniquely id.
        pats = m.get_patients_from_name("Peter","Django","8888")
        assert 1 == len(pats)
        assert 'Django' == pats[0].last_name



    def test_patient_by_id (self):

        m = ModelObjects()
        pat1 = m.patients[0]
        assert pat1 != None
        pp = m.get_patient_by_id(pat1.id)
        print(id(pat1), id(pp))
        # verify they are same.
        assert pp == pat1

        pp = m.get_patient_by_id(-34)
        assert None == pp
