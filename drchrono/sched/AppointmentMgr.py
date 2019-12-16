from drchrono.model2.Appointment import Appointment
from drchrono.model2.PatientAppointment import PatientAppointment
from drchrono.sched.ModelObjects import ModelObjects

class AppointmentMgr:

    # TODO methods below should go into some inner classes for Appointments and Patients

    # write the appointment to datastore.  It will not have an id and will return an Appointment object
    # which results from the writing (e.g. with id)
    @staticmethod
    def create_appointment (appointment):
        return ModelObjects().create_appointment(appointment)



    @staticmethod
    def set_appointment_status(appointment_id, status, persist=False):
        appointment_id = int(appointment_id)
        m = ModelObjects()
        appt = m.appointments_map[appointment_id] #type: Appointment
        appt.status = status
        if persist:
            m.save_appointment_status(appointment_id, status)

    @staticmethod
    def set_rating (appointment_id, rating):
        extra = {'rating': rating}
        ModelObjects().set_extra(appointment_id, extra)

    @staticmethod
    def get_most_recent_complete_appointment (patient_id):
        '''
        Get the most recently completed appointment for this patient
        :param patient_id:
        :return:
        '''
        m = ModelObjects()

        max_dt = None
        complete_apts = [a for a in AppointmentMgr.get_patient_appointments(patient_id) if a.status == Appointment.STATUS_COMPLETE]
        complete_apts = sorted(complete_apts, reverse=True, key=lambda a: a.scheduled_time)
        return complete_apts[0] if len(complete_apts) > 0 else None

    @staticmethod
    def get_patient_appointments (patient_id=None):
        '''
        :return: List[PatientAppointment] objects for today sorted by scheduled time
        '''
        patient_id = int(patient_id) if patient_id else None
        m = ModelObjects()

        res = []
        pas = m.appointments #type: List[PatientAppointment]
        for a in pas:
            pid = a.patient_id
            if patient_id and pid != patient_id:
                continue
            p = m.patients_map[pid]
            pa = PatientAppointment(patient=p, appointment=a)
            res.append(pa)
        return sorted(res, key=lambda pa: pa.scheduled_time)