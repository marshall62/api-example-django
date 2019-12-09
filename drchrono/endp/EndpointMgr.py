import os
from drchrono.endp import mock_endpoints as mock
from drchrono.endp import endpoints as api


class EndpointMgr:
    use_mock = os.environ['USE_MOCK_ENDPOINTS']

    @classmethod
    def patient (cls):
        if cls.use_mock:
            return mock.Patient_MockEndpoint
        else:
            return api.PatientEndpoint

    @classmethod
    def appointment(cls):
        if cls.use_mock:
            return mock.Appointment_MockEndpoint
        else:
            return api.AppointmentEndpoint

    @classmethod
    def doctor(cls):
        if cls.use_mock:
            return mock.Doctor_MockEndpoint
        else:
            return api.DoctorEndpoint

    @classmethod
    def office(cls):
        if cls.use_mock:
            return mock.Office_MockEndpoint
        else:
            return api.OfficeEndpoint




