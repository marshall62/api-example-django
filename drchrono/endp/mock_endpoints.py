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

    def list (self, params={}, verbose=False, **kwargs):
        for prop, val in kwargs.items():
            params[prop]=val
        res = []
        for rec in self.data_list:
            fail = False
            for prop,val in params.items():
                v2 = rec.get(prop)
                if v2 != val:
                    fail = True
                    break
            if not fail:
                yield rec
        return res

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

class Appointment_MockEndpoint(MockEndpoint):

    def __init__(self, *args):
        super().__init__('appointments.txt')

    def list(self, params={}, verbose=False, date=None):
        # override so this can ignore the date and just return all appointments (assuming we are always getting todays appts)
        return super().list(params=params,verbose=verbose)

