import abc

class DataStoreAbstract(abc.ABC):

    @abc.abstractmethod
    def reload_patients (self):
        pass

    @abc.abstractmethod
    def reload_appointments (self):
        pass

    @abc.abstractmethod
    def update_patient (self, patient_id, new_data=None):
        pass

    @abc.abstractmethod
    def create_appointment (self, appt_data):
        pass

    @abc.abstractmethod
    def save_appointment_status (self, appt_id, status):
        pass

    @abc.abstractmethod
    def save_appointment_extra (self, appt_id, extra):
        pass