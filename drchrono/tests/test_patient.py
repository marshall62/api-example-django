import pytest
from drchrono.api_models.Patient import Patient
from drchrono.api_models.Doctor import Doctor
from drchrono.sched.Patients import Patients
from drchrono.endpoints import PatientEndpoint
from drchrono.exc.exceptions import NotFoundException, NonUniqueException
from .api_access import get_access_tok

class TestPatient:

    def setup_class(cls):
        cls.doctor = Doctor()
        cls.pf = Patients(cls.doctor)
        cls.patients = cls.pf.patients
        cls.patient_endpoint = PatientEndpoint(get_access_tok())

        # create a second Peter Django with ssn 8888 if not there
        try:
            pj = Patient(first_name='Peter', last_name='Django', ssn4='8888')
        except NotFoundException:
            p2 = Patient()
            p2.data['first_name'] = 'Peter'
            p2.data['last_name'] = 'Django'
            p2.data['social_security_number'] = '888-88-8888'
            p2.data['gender'] = 'Male'
            p2.data['doctor'] = cls.doctor.id
            p2.create()

    def teardown_class (cls):
        pass

    def test_doctor_patients (self):
        for p in TestPatient.patients:
            print(p)
        assert len(TestPatient.patients) != 0

    def test_patient_name_error (self):
        '''test a failed lookup'''
        with pytest.raises(NotFoundException):
            p = Patient(first_name='dennis', last_name='martine') # bad lname

        # create a second dennis martin with a different ssn
        # then check that a lookup by f/lname will return non-unique exception
        with pytest.raises(NonUniqueException):
            # There are two Peter Djangos
            p = Patient(first_name='Peter', last_name='Django')

        # this lookup should succeed because we include ssn to uniquely id.
        p = Patient(first_name='Peter', last_name='Django', ssn4='8888' )
        assert type(p) == Patient
        assert 'Django' == p.last_name

    # need a test for a patient that has a non-unique name requiring an ssn4


    def test_patient (self):

        p = TestPatient.pf.get_patient1() # get first of whoever is listed as a patient of this doctor
        assert p != None
        pp = Patient(id=p.id)  # use API to lookup this patient id.
        # verify they are same.
        for k,v in p.data.items():
            if k == 'patient_photo':  # these seem to be generated dynamically and are different
                continue
            assert pp.data[k] == v, "Failed while comparing key {} value1: {} value2: {}".format(k,v,pp.data[k])

