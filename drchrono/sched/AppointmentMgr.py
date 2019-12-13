from drchrono.model2.Appointment import Appointment
from drchrono.sched.ModelObjects import ModelObjects
class AppointmentMgr:

    # TODO methods below should go into some inner classes for Appointments and Patients

    # write the appointment to the api.  It will not have an id
    @staticmethod
    def save_appointment (appointment):
        m = ModelObjects()
        rec = m.api_gateway.create_appointment(appointment.data)
        apt = Appointment(rec)
        m.appointments.append(apt)
        m.appointments_map[apt.id] = apt
        return apt

    @staticmethod
    def set_appointment_status(appointment_id, status, persist=False):
        '''
        Modifies the Appointment object held here which also modifies its underlying data dictionary held in
        the APIGateway cache.
        :param appointment_id:
        :param status:
        :param persist: If True, the status will be written to the API
        :return:
        '''
        m = ModelObjects()
        appt = m.appointments_map[appointment_id] #type: Appointment
        appt.status = status
        if persist:
            m.api_gateway.save_appointment_stat(appointment_id)

    @staticmethod
    def get_most_recent_complete_appointment (patient_id):
        '''
        Get the most recently completed appointment for this patient
        :param patient_id:
        :return:
        '''
        m = ModelObjects()

        max_dt = None
        complete_apts = [a for a in m.doctor.get_patient_appointments(patient_id) if a.status == Appointment.STATUS_COMPLETE]
        complete_apts = sorted(complete_apts, reverse=True, key=lambda a: a.scheduled_time)
        return complete_apts[0] if len(complete_apts) > 0 else None

