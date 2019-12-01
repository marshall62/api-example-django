from drchrono.models.Patient import Patient
from drchrono.models.Doctor import Doctor
from drchrono.sched.Patients import Patients

class TestPatient:

    def setup_class(cls):
        cls.doctor = Doctor()
        cls.pf = Patients(cls.doctor)
        cls.patients = cls.pf.patients


    def test_doctor_patients (self):
        for p in TestPatient.patients:
            print(p)
        assert len(TestPatient.patients) != 0


    def test_patient (self):

        p = TestPatient.pf.get_patient1() # get first of whoever is listed as a patient of this doctor
        assert p != None
        pp = Patient(id=p.id) # use API to lookup this patient id.
        # verify they are same.
        for k,v in p.data.items():
            if k == 'patient_photo':  # these seem to be generated dynamically and are different
                continue
            assert pp.data[k] == v, "Failed while comparing key {} value1: {} value2: {}".format(k,v,pp.data[k])

