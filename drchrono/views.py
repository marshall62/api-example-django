from django.views.generic import TemplateView, FormView, View
from django.shortcuts import render
from django.urls import reverse_lazy
from drchrono.sched.DaySchedule import DaySchedule
from drchrono.models.Doctor import Doctor
from drchrono.models.Patient import Patient
from drchrono.forms import CheckinForm


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
        patient_appts = sched.get_all_patient_appointments()
        kwargs['doctor'] = doc.obj
        kwargs['appointments'] = patient_appts
        return kwargs




class Kiosk(View):
    """
    The patient check-in Kiosk.
    """
    template_name = 'kiosk.html'

    def get (self, request, *args, **kwargs):
        doc = Doctor()  # TODO We should instead look this up once at start of app and hold statically
        kwargs['doctor'] = doc.obj
        return render(request, self.template_name)

    def post (self, request, *args, **kwargs):
        post = request.POST
        doc = Doctor()
        fname = post['fname']
        lname = post['lname']
        ssn4 = post['ssn4']
        p = Patient()
        pdata = p.get_patient(fname, lname, ssn4)
        if not pdata:
            print("patient not found", fname, lname, ssn4)
        else:
            schedule = DaySchedule(doc.id)
            appts = schedule.get_patient_appointments(pdata['id'])
            for a in appts:
            # if patient has multiple appts set all that are non-complete to "Checked In"
            # This just makes it so the patient does not have to sign in thru the kiosk again.
                if a['status'] != 'Complete' and a['status'] != 'Checked In':
                    print('appointment id', a['id'], 'status', a['status'])
                    schedule.set_patient_appointment_status(a['id'], 'Checked In')
        # TODO send to a screen to update their info if found
        # else need to reprompt if not found
        doc = Doctor()
        kwargs['doctor'] = doc.obj
        return  render(request, self.template_name)


    # def get_context_data(self, **kwargs):
    #     kwargs = super(Kiosk, self).get_context_data(**kwargs)
    #     doc = Doctor()
    #     kwargs['doctor'] = doc.obj
    #     return kwargs

class CheckinView(FormView):
    form_class = CheckinForm
    template_name = 'checkin.html'
    success_url = reverse_lazy('kiosk')

    def form_valid (self, form):
        self.checkin_patient(form.cleaned_data)
        return super(CheckinView, self).form_valid(form)

    def checkin_patient (self, valid_data):
        print("patient checking in", valid_data)