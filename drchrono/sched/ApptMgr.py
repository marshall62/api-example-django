from drchrono.endp.endpoints import *
import drchrono.token as token
import datetime
from .APIGateway import APIGateway

class ApptMgr:
    class __ApptMgr:
        def __init__(self):
            self.api_gateway = APIGateway()

    instance = None

    def __new__(cls, use_api=True):
        if not ApptMgr.instance:
            ApptMgr.instance = ApptMgr.__ApptMgr(use_api=use_api)
        return ApptMgr.instance

    def reload_patients (self):
        self.api_gateway.load_pts_from_api()

    def reload_appointments (self):
        self.api_gateway.load_appts_from_api()

    def get_doctor_map (self):
        self.instance._api_gateway

    def to_map (self, obj_list):
        '''
        :param obj_list: a list of objects as given back by api.list method
        :return: return a map id->object based on ids in the objects.
        '''
        return {o['id']: o for o in obj_list}

    @property
    def doctor(self):
        return self.instance._doctor

    @property
    def office(self):
        return self.instance._office

    @property
    def appointments(self):
        return self.instance._appointments

    @property
    def patients(self):
        return self.instance._patients

    # def __getattr__(self, name):
    #     return getattr(self.instance, name)
    # def __setattr__(self, name):
    #     return setattr(self.instance, name)


