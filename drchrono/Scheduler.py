from drchrono.model2.Appointment import Appointment
from drchrono.sched.ModelObjects import ModelObjects
from drchrono import dates as dateutil
from drchrono.api_models.PatientAppointment import PatientAppointment
from django.http import HttpResponse
from django.http import JsonResponse

def get_appts (request):
    sched = Scheduler.get_appointments(request) # dict of appointments keyed by status
    avg_wt, max_wt = Scheduler.get_avg_and_max_wait_time()
    avg_duration = Scheduler.get_avg_duration()
    stats = {'avg_wait': dateutil.min2minSec(avg_wt),
             'max_wait': dateutil.min2minSec(max_wt),
             'avg_duration': dateutil.min2minSec(avg_duration)}
    sched['stats'] = stats
    return JsonResponse(sched)

def update_stat (request, appointment_id):
    return Scheduler.update_appointment_status(request, appointment_id)


class Scheduler:

    update_count = 0

    @classmethod
    def get_avg_and_max_wait_time (cls):
        ''' Compute the average wait time of all completed appointments for TODAY
        :return minutes
        '''
        doc = ModelObjects().doctor
        mx = 0
        tot = 0
        count = 0
        for pa in doc.get_patient_appointments():
            if pa.status == Appointment.STATUS_COMPLETE:
                sch = pa.scheduled_time
                comp = pa.completion_time_raw
                min, sec = dateutil.time_diff(comp, sch)
                if min > mx:
                    mx = min
                tot += min # ignore secs
                count += 1
        if count > 0:
            return tot // count, mx
        else:
            return 0, mx


    @classmethod
    def get_avg_duration (cls):
        ''' Compute the average actual duration time of all completed appointments for TODAY'
        :return minutes
        '''
        doc = ModelObjects().doctor
        tot = 0
        count = 0
        for pa in doc.get_patient_appointments():
            if pa.status == Appointment.STATUS_COMPLETE:
                min, sec = pa.actual_duration_raw
                tot += min # ignore secs
                count += 1
        if count > 0:
            return tot // count
        else:
            return 0

    @classmethod
    def update_from_api (cls):
        # get new list of appointments every time browser page calls for updates
        #
        m = ModelObjects()
        m.reload_appointments()

        # patients are loaded every 10 updates because this is less dynamic
        if Scheduler.update_count % 10 == 0:
            m.reload_patients()

    @classmethod
    def get_appointments (cls, request):
        # pas = Appointments.get_active_appointments_for_date() #type: # List[PatientAppointment]
        '''
        This is called on a timer from the UI.
        :param request:
        :return:
        '''
        Scheduler.update_count += 1
        Scheduler.update_from_api()
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
            m = ModelObjects()
            m.set_appointment_status(appointment_id,status,persist=True) #save status locally and in API
            return HttpResponse()