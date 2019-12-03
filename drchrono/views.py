from django.views.generic import TemplateView, FormView, View
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from drchrono.models.Doctor import Doctor
from drchrono.models.Appointment import Appointment
from drchrono.sched.Appointments import Appointments
from drchrono.models.Patient import Patient
from drchrono.forms import CheckinForm, PatientInfoForm
import django.forms.forms
from django.forms.utils import ErrorList

from drchrono.exc.exceptions import NonUniqueException, NotFoundException
from django import forms

def updateAppointmentStatus (request, appointment_id):
    if request.method == 'POST':
        status = request.POST['status']
        trans = {'absent': 'No Show', 'complete': 'Complete', 'waiting': 'Checked In', 'exam': 'In Session'}
        status = trans[status];
        a = Appointment(id=appointment_id)
        a.status = status # writes status to appointment API
        return HttpResponse()



class SetupView(TemplateView):
    """
    The beginning of the OAuth sign-in flow. Logs a user into the kiosk, and saves the token.
    """
    template_name = 'kiosk_setup.html'


class DoctorSchedule(TemplateView):
    """
    The doctor can see what appointments they have today.
    """
    template_name = 'doctor_schedule.html'


    def get_context_data(self, **kwargs):
        kwargs = super(DoctorSchedule, self).get_context_data(**kwargs)
        doc = Doctor()
        appts = Appointments(doc)
        today_appts = appts.get_active_appointments_for_date()
        kwargs['doctor'] = doc
        kwargs['appointments'] = today_appts
        return kwargs




class Kiosk(View):
    """
    The patient check-in Kiosk.
    """
    template_name = 'kiosk.html'

    def get (self, request, *args, **kwargs):
        doc = Doctor()
        kwargs['doctor'] = doc
        return render(request, self.template_name)

    # def get_context_data(self, **kwargs):
    #     kwargs = super(Kiosk, self).get_context_data(**kwargs)
    #     doc = Doctor()
    #     kwargs['doctor'] = doc.obj
    #     return kwargs

class CheckinView(FormView):
    form_class = CheckinForm
    template_name = 'checkin.html'
    # success_url = reverse_lazy('patient_info')
    success_url = 'patientInfo'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request,self.template_name, {'form': form})

    def post (self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            try:
                pat = self.checkin_patient(form)
                if pat:
                    return redirect(self.success_url,
                                    patient_id=pat.id)
            except Exception as e:
                print(e)
                form.errors[django.forms.forms.NON_FIELD_ERRORS] = ErrorList([e.__str__()])
        return render(request, self.template_name, {'form': form})



    def checkin_patient (self, form):
        valid_data = form.cleaned_data
        fname = valid_data['first_name']
        lname = valid_data['last_name']
        ssn4 = valid_data['ssn4']

        p = Patient(first_name=fname, last_name=lname, ssn4=ssn4)
        # TODO SHould we verify that this patient has an appointment today and that they have arrived in neighborhood of scheduled time?
        p.status = 'Checked In' # this could generate an error that isn't processed correctly
        return p





class PatientInfoView (FormView):
    form_class = PatientInfoForm
    template_name = 'patient_info.html'
    success_url = reverse_lazy('patientCheckIn')

    def get(self, request, patient_id):
        p = Patient(id=patient_id)
        f = self.form_class(p.data)
        return render(request, self.template_name, {'fname': p.first_name, 'form': f})
