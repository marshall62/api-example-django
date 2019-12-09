from drchrono.endp.endpoints import BaseEndpoint
import drchrono.settings as settings
import json
import os

class MockEndpoint (BaseEndpoint):


    def __init__ (self, filename):
        self.data_list = []
        self.max_id = -1
        filename = os.path.join(settings.SOURCE_DIR , 'tests', filename)
        with open(filename, 'r') as f:
            for l in f:
                record = json.loads(l)
                # dumped json has strings containing ints written as ints but API has all ints within strings so we need to mimic
                for k,v in record.items():
                    if type(v) == int:
                        record[k] = str(v)
                if int(record['id']) > self.max_id:
                    self.max_id = int(record['id'])
                self.data_list.append(record)

    def create(self, data=None, json=None, **kwargs):
        self.max_id += 1
        data['id'] = str(self.max_id)
        self.data_list.append(data)
        return data

    def fetch(self, id, params=None, **kwargs):
        for rec in self.data_list:
            if rec['id'] == id:
                return rec
        return None

    def list (self, params=None, verbose=False, **kwargs):
        if not params:
            params = {}
        for prop, val in kwargs.items():
            params[prop]=val
        for rec in self.data_list:
            fail = False
            for prop,val in params.items():
                v2 = rec.get(prop)
                if type(v2) == str:
                    v2 = v2.lower()
                if type(val) == str:
                    val = val.lower()
                if v2 != val:
                    fail = True
                    break
            if not fail:
                yield rec

    def update(self, id, data, partial=True, **kwargs):
        found = None
        for i, rec in enumerate(self.data_list):
            if rec['id'] == id:
                found = rec
                break
        if found:
            if partial:
                for prop, val in kwargs.items():
                    rec[prop] = val
                for prop, val in data.items():
                    rec[prop] = val
            else:
                self.data_list[i] = data
        return data


class Office_MockEndpoint (MockEndpoint):

    def __init__ (self, *args):
        self.data_list = [{'id': '1', 'doctor': '254819'}]

class Doctor_MockEndpoint (MockEndpoint):

    def __init__ (self, *args):
        super().__init__('doctor.txt')


class Patient_MockEndpoint(MockEndpoint):

    def __init__(self, *args):
        super().__init__('patients.txt')

    def list(self, params=None, first_name=None, last_name=None, ssn4=None, **kwargs):
        params = params or {}
        if first_name:
            params['first_name'] = first_name
        if last_name:
            params['last_name'] = last_name
        patients = super().list(params=params, **kwargs)
        if ssn4:
            return [p for p in patients if p['social_security_number'][-4:] == ssn4]
        else:
            return list(patients)

class Appointment_MockEndpoint(MockEndpoint):

    def __init__(self, *args):
        super().__init__('appointments.txt')

    def list(self, params=None, verbose=False, date=None):
        # override so this can ignore the date and just return all appointments (assuming we are always getting todays appts)
        return list(super().list(params=params,verbose=verbose))

