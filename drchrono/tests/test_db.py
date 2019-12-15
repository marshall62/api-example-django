from drchrono.models import *
import pytest

@pytest.mark.django_db
def test_patient_read ():
    p = Patient(data="some garbage")
    p.save()
    assert Patient.objects.all().count() == 1

    p = Patient(data="some more garbage")
    p.save()
    assert Patient.objects.all().count() == 2



