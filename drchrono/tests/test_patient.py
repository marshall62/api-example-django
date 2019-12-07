import pytest
from drchrono.api_models.Patient import Patient
from drchrono.api_models.Doctor import Doctor
from drchrono.exc.exceptions import NotFoundException, NonUniqueException
from .api_access import get_access_tok

class TestPatient:

    def setup_class(cls):
        cls.doctor = Doctor()
        cls.patients = cls.doctor.get_patients()

        # create a second Peter Django with ssn 8888 if not found
        try:
            cls.patient1 = Patient(first_name='Peter', last_name='Django', ssn4='8888')
        except NotFoundException:
            cls.patient1 = Patient.create(first_name='Peter', last_name='Django',social_security_number='888-88-8888',gender='Male', doctor=cls.doctor.id)

    def teardown_class (cls):
        '''
        deleting Peter Django created above is not allowed by API for this account.
        '''
        # TODO delete test Patient created above
        pass



    def test_patient_name_error (self):
        '''test a failed lookup'''
        with pytest.raises(NotFoundException):
            Patient(first_name='dennis', last_name='martine') # bad lname

        # create a second dennis martin with a different ssn
        # then check that a lookup by f/lname will return non-unique exception
        with pytest.raises(NonUniqueException):
            # There are two Peter Djangos
            Patient(first_name='Peter', last_name='Django')

        # this lookup should succeed because we include ssn to uniquely id.
        p = Patient(first_name='Peter', last_name='Django', ssn4='8888' )
        assert type(p) == Patient
        assert 'Django' == p.last_name

    # need a test for a patient that has a non-unique name requiring an ssn4


    def test_patient (self):

        p = self.patient1
        assert p != None
        pp = Patient(id=p.id)  # use API to lookup this patient id.
        # verify they are same.
        for k,v in p.data.items():
            if k == 'patient_photo':  # these seem to be generated dynamically and are different
                continue
            assert pp.data[k] == v, "Failed while comparing key {} value1: {} value2: {}".format(k,v,pp.data[k])

