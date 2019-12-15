from drchrono.endp.endpoints import *
from drchrono.datastore.DataStoreAbstract import DataStoreAbstract
from drchrono.apitoken import get_token
import datetime

class APIGateway:

    instance = None

    def __new__(cls, doLoad=True):
        if not APIGateway.instance:
            APIGateway.instance = APIGateway.__APIGateway(doLoad)
        return APIGateway.instance



    def __getattr__(self, name):
        return getattr(self.instance, name)

    class __APIGateway(DataStoreAbstract):

        def __init__ (self, doLoad):
            if doLoad:
                self.doctor = self._load_dr_from_api()
                self.office = self._load_office_from_api()
                self._load_pts_from_api()
                self._load_appts_from_api()


        def reload_patients (self):
            return self._load_pts_from_api()

        def reload_appointments (self):
            temp_map = self.appointments_map
            res = self._load_appts_from_api()
            # this is how I preserve my extra fields that don't read/write to API
            # put whatever extras there were into the newly loaded appointments.
            print('checking for extra in data')
            for id, data in temp_map.items():
                if 'extra' in data:
                    print('found extra ', data['extra'])
                    self.appointments_map[id]['extra'] = data['extra']
            return res

        def _as_map (self, obj_list):
            return {int(o['id']): o for o in obj_list}

        def _load_dr_from_api (self):
            ep = DoctorEndpoint(get_token())
            return next(ep.list())

        def _load_pts_from_api (self):
            ep = PatientEndpoint(get_token())
            self.patients = ep.list(doctor_id=self.doctor['id'])
            self.patients_map = self._as_map(self.patients)
            return self.patients

        def _load_appts_from_api (self):
            ep = AppointmentEndpoint(get_token())
            today_ymd = datetime.date.today().strftime('%Y-%m-%d')
            self.appointments = ep.list(verbose=True, date=today_ymd, doctor_id= self.doctor['id'])
            self.appointments_map = self._as_map(self.appointments)
            return self.appointments

        def _load_office_from_api (self):
            ep = OfficeEndpoint(get_token())
            doc_id = self.doctor['id']
            dr_offices = [o for o in ep.list() if o['doctor'] == doc_id]
            assert 0 < len(dr_offices), "No offices for doctor {}".format(doc_id)
            return  dr_offices[0]

        def update_patient_summary (self, pat_data):
            ep = PatientSummaryEndpoint(get_token())
            ep.update(id=pat_data['id'], data=pat_data, partial=True)


        def update_patient (self, patient_id, new_data=None):
            ep = PatientEndpoint(get_token())
            if new_data:
                ep.update(id=str(patient_id), data=new_data, partial=True)


        def create_appointment (self, appt_data):
            ep = AppointmentEndpoint(get_token())
            json = ep.create(data=appt_data)
            self.appointments.append(json)
            self.appointments_map[int(json['id'])] = json
            return json

        def save_appointment_status (self, appt_id, status):
            '''
            :param appt_id:
            :param status:
            :return:
            '''
            # self.appointments_as_map[appt_id]['status'] = status # change the value in the cache
            ep = AppointmentEndpoint(get_token())
            a = self.appointments_map[appt_id]
            ep.update(id=str(appt_id), data={'status': status}, partial=True)

        def save_appointment_extra (self, appt_id, extra):
            rec = self.appointments_map[int(appt_id)]
            rec['extra'] = extra

