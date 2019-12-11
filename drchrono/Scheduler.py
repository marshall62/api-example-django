from drchrono.model2.Appointment import Appointment
from drchrono.sched.Appointments import Appointments
import drchrono.sched.APIGateway
from drchrono.sched.ModelObjects import ModelObjects
from drchrono.api_models.PatientAppointment import PatientAppointment
from django.http import HttpResponse
from django.http import JsonResponse
from collections import defaultdict

def get_appts (request):
    return Scheduler.get_appointments(request)

def update_stat (request, appointment_id):
    return Scheduler.update_appointment_status(request, appointment_id)


class Scheduler:

    update_count = 0

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
        return JsonResponse(schedule)

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