from drchrono.api_models.Doctor import Doctor
from drchrono.api_models.Appointment import Appointment
from drchrono.sched.Appointments import Appointments
import json

def dump_appts ():
    with open('appointments.txt','w') as fh:
        aps = Appointments.get_appointments_for_date()
        for a in aps:
            s = json.dumps(a.appointment.data)
            fh.write(s+'\n')

def dump_pats ():
    with open('patients.txt','w') as fh:
        pats = Doctor().get_patients()
        for p in pats:
            s = json.dumps(p.data)
            fh.write(s+'\n')


def dump_doc ():
    with open('doctor.txt', 'w') as fh:
        d = Doctor()
        fh.write(json.dumps(d.data))


def test():
    Appointments.set_doctor(Doctor())
    dump_appts()
    dump_pats()
    dump_doc()

