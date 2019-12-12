from drchrono.endp.endpoints import *
from drchrono.token import get_token
import datetime

class APIGateway:

    instance = None

    def __new__(cls, doLoad=True):
        if not APIGateway.instance:
            APIGateway.instance = APIGateway.__APIGateway(doLoad)
        return APIGateway.instance



    def __getattr__(self, name):
        return getattr(self.instance, name)

    class __APIGateway:

        def __init__ (self, doLoad):
            if doLoad:
                self.doctor = self._load_dr_from_api()
                self.office = self._load_office_from_api()
                self._load_pts_from_api()
                self._load_appts_from_api()


        def reload_patients (self):
            return self._load_pts_from_api()

        def reload_appointments (self):
            return self._load_appts_from_api()

        def _as_map (self, obj_list):
            return {o['id']: o for o in obj_list}

        def _load_dr_from_api (self):
            ep = DoctorEndpoint(get_token())
            return next(ep.list())

        def _load_pts_from_api (self):
            ep = PatientEndpoint(get_token())
            self.patients = ep.list(params={'doctor': self.doctor['id']})
            self.patients_map = self._as_map(self.patients)
            return self.patients

        def _load_appts_from_api (self):
            ep = AppointmentEndpoint(get_token())
            today_ymd = datetime.date.today().strftime('%Y-%m-%d')
            self.appointments = ep.list(verbose=True, date=today_ymd, params={'doctor': self.doctor['id']})
            self.appointments_map = self._as_map(self.appointments)
            return self.appointments

        def _load_office_from_api (self):
            ep = OfficeEndpoint(get_token())
            doc_id = self.doctor['id']
            dr_offices = [o for o in ep.list() if o['doctor'] == doc_id]
            assert 0 < len(dr_offices), "No offices for doctor {}".format(doc_id)
            return  dr_offices[0]


        def create_appointment (self, appt_data):
            ep = AppointmentEndpoint(get_token())
            json = ep.create(data=appt_data)
            self.appointments.append(json)
            self.appointments_map[json['id']] = json
            return json

        def save_appointment_stat (self, appt_id):
            '''
            Will write the current status of the appointment to the API.
            Will write it regardless of whether its changed or not (TODO add some kind of flag to know if object is changed)
            :param appt_id:
            :param status:
            :return:
            '''
            # self.appointments_as_map[appt_id]['status'] = status # change the value in the cache
            ep = AppointmentEndpoint(get_token())
            a = self.appointments_map[appt_id]
            stat = a['status']
            ep.update(id=appt_id, data={'status': stat}, partial=True)

        def get_appointment_status_transition (self, appt_id, status):
            # TODO if there are many with the same status, it returns first one.  Not sure of the
            # ordering in this list, but probably want the one with the latest timestamp.
            rec = self.appointments_map[appt_id]
            trans = rec['status_transitions']
            for t in trans:
                if t['to_status'] == status:
                    return t
            return None