from drchrono.endp.endpoints import AppointmentEndpoint, DoctorEndpoint
from drchrono.token import get_token


def test_appt ():
    ep = DoctorEndpoint(get_token())
    doc = next(ep.list())
    ep = AppointmentEndpoint(get_token())

    all = ep.list(date='2019-12-12')
    for a in all:
        print(a)
    assert len(all) > 0