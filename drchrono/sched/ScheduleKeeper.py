from drchrono.model2.Appointment import Appointment
from drchrono.sched.AppointmentMgr import AppointmentMgr
from drchrono.sched.ModelObjects import ModelObjects
from drchrono import dates as dateutil
import drchrono.endp.endpoints as ep
from drchrono.model2.PatientAppointment import PatientAppointment
from django.http import HttpResponse
from django.http import JsonResponse

def get_appts (request):
    sched = ScheduleKeeper.get_appointments(request) # dict of appointments keyed by status
    sched['stats'] = ScheduleKeeper.get_appointment_stats()
    sched['network_on'] = 1 if ep.BaseEndpoint.WORKING else 0
    return JsonResponse(sched)

def update_stat (request, appointment_id):
    return ScheduleKeeper.update_appointment_status(request, appointment_id)

def toggle_net (request):
    # turn on/off simulation of network failure.
    ep.BaseEndpoint.WORKING = not ep.BaseEndpoint.WORKING
    return JsonResponse({'network_status': ep.BaseEndpoint.WORKING})


class ScheduleKeeper:

    update_count = 0

    @classmethod
    def get_appointment_stats (cls):
        ''' Compute stats about completed appointments
        '''
        # return {'max_wait': 0, 'avg_wait': 0, 'avg_duration': 0}
        doc = ModelObjects().doctor
        mx = 0
        duration_total = 0
        wait_total = 0
        count = 0
        for pa in doc.get_patient_appointments():
            if pa.status == Appointment.STATUS_COMPLETE:
                sch = pa.scheduled_time
                comp = pa.completion_time_raw
                min, sec = pa.actual_duration_raw
                duration_total += min
                min, sec = dateutil.time_diff(comp, sch)
                wait_total += min # ignore secs
                if min > mx:
                    mx = min
                count += 1
        if count > 0:
            return {'max_wait': mx, 'avg_wait': wait_total // count, 'avg_duration': duration_total // count}
        else:
            return {'max_wait': 0, 'avg_wait': 0, 'avg_duration': 0}


    @classmethod
    def _refresh_appointments_and_patients_from_api (cls):
        # get new list of appointments every time browser page calls for updates
        #
        m = ModelObjects()
        m.reload_appointments()

        # patients are loaded every 10 updates because this is less dynamic
        if ScheduleKeeper.update_count % 10 == 0:
            m.reload_patients()

    @classmethod
    def get_appointments (cls, request):
        '''
        This is called on a timer from the UI.
        :param request:
        :return:
        '''
        ScheduleKeeper.update_count += 1
        ScheduleKeeper._refresh_appointments_and_patients_from_api()
        doc = ModelObjects().doctor

        pas = doc.get_patient_appointments() #type: List[PatientAppointment]
        # remove the appointments in the waiting room and the ones in exam so that we have the appointments for the day
        # that are active.
        schedule = {'exam': [], 'waiting': [], 'complete': [], 'upcoming': []}
        for pa in pas:
            if pa.status == Appointment.STATUS_EXAM:
                schedule['exam'].append(pa.toJSON()) # unused by UI but including for completeness
            elif pa.status == Appointment.STATUS_COMPLETE:
                schedule['complete'].append(pa.toJSON())
            elif pa.status == Appointment.STATUS_WAITING:
                schedule['waiting'].append(pa.toJSON())
            else:
                schedule['upcoming'].append(pa.toJSON())
        return schedule


    def update_appointment_status (request, appointment_id):
        if request.method == 'POST':
            status = request.POST['status']
            trans = {'absent': Appointment.STATUS_NO_SHOW,
                     'complete': Appointment.STATUS_COMPLETE,
                     'waiting': Appointment.STATUS_WAITING,
                     'exam': Appointment.STATUS_EXAM}
            status = trans[status];
            AppointmentMgr.set_appointment_status(appointment_id,status,persist=True) #save status locally and in API
            return HttpResponse()