from django.views.generic import TemplateView
from sched.DaySchedule import DaySchedule
from models.Doctor import Doctor


class SetupView(TemplateView):
    """
    The beginning of the OAuth sign-in flow. Logs a user into the kiosk, and saves the token.
    """
    template_name = 'kiosk_setup.html'


class DoctorWelcome(TemplateView):
    """
    The doctor can see what appointments they have today.
    """
    template_name = 'doctor_welcome.html'


    def get_context_data(self, **kwargs):
        kwargs = super(DoctorWelcome, self).get_context_data(**kwargs)
        doc = Doctor()
        sched = DaySchedule(doc.id)
        patient_appts = sched.get_patient_appointments()
        kwargs['doctor'] = doc.obj
        kwargs['appointments'] = patient_appts
        return kwargs




class Kiosk(TemplateView):
    """
    The patient check-in Kiosk.
    """
    template_name = 'kiosk.html'


    def get_context_data(self, **kwargs):
        kwargs = super(Kiosk, self).get_context_data(**kwargs)
        doc = Doctor()
        kwargs['doctor'] = doc.obj
        return kwargs