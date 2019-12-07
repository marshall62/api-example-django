from drchrono.api_models.Appointment import Appointment
from drchrono.sched.Appointments import Appointments
from drchrono.api_models.PatientAppointment import PatientAppointment
from django.http import HttpResponse
from django.http import JsonResponse
import pprint

def get_appointments (request):
    pas = Appointments.get_active_appointments_for_date() #type: List[PatientAppointment]
    # remove the appointments in the waiting room and the ones in exam so that we have the appointments for the day
    # that are active.
    schedule = {'upcoming': [], 'waiting': []}
    for pa in pas:
        if pa.status == 'In Session':
            continue
        elif pa.status == 'Checked In':
            schedule['waiting'].append(pa.toJSON())
        else:
            schedule['upcoming'].append(pa.toJSON())

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint('-'*80)
    pp.pprint(schedule)
    return JsonResponse(schedule)

def update_appointment_status (request, appointment_id):
    if request.method == 'POST':
        status = request.POST['status']
        trans = {'absent': 'No Show', 'complete': 'Complete', 'waiting': 'Checked In', 'exam': 'In Session'}
        status = trans[status];
        a = Appointment(id=appointment_id)
        a.status = status # writes status to appointment API
        return HttpResponse()