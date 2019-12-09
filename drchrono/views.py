from django.views.generic import TemplateView, FormView, View
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from drchrono.api_models.Doctor import Doctor
from drchrono.sched.Appointments import Appointments
from drchrono.api_models.Patient import Patient
from drchrono.forms import CheckinForm, PatientInfoForm, CheckoutSurveyForm
import django.forms.forms
from django.forms.utils import ErrorList






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
        today_appts = Appointments.get_active_appointments_for_date()
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
    checkin_success_url = 'patientInfo'
    checkout_success_url = 'checkout'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request,self.template_name, {'form': form})

    def post (self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            if request.POST.get('checkin'):
                try:
                    pat = self.checkin_patient(form)
                    if pat:
                        return redirect(self.checkin_success_url,
                                        patient_id=pat.id)
                except Exception as e:
                    print(e)
                    form.errors[django.forms.forms.NON_FIELD_ERRORS] = ErrorList([e.__str__()])
            else:
                pat = self.get_patient(form)
                if pat:
                    return redirect(self.checkout_success_url,
                                    patient_id=pat.id)
        return render(request, self.template_name, {'form': form})



    def get_patient (self, form):
        valid_data = form.cleaned_data
        fname = valid_data['first_name']
        lname = valid_data['last_name']
        ssn4 = valid_data['ssn4']
        p = Patient(first_name=fname, last_name=lname, ssn4=ssn4)
        return p

    def checkin_patient (self, form):
        '''
        Check in a patient.
        Assumptions:  Patient may have more than one appointment today.  Any appointments with status != Complete or Cancelled
        will be marked as status = Checked In.

        Issues:  If the patient has many appointments it would make sense to complete the first, and perhaps return
        to the waiting room.  This is handled correctly because that next appointment is marked as Checked In.

        If however, there is a large gap between appts, the patient probably leaves after completing the first one.
        For the next appt, s/he is marked Checked In which is now an inaccurate reflection of reality.
        Two possible outcomes follow:
            -S/He doesn't show up (at all or on time):  Dr will mark as no-show
            -S/He arrives back in time: Dr admits and completes.

        So marking all appointments as Checked In seems to work well for this odd (rare) multiple-appt use-case
        :param form:
        :return:
        '''
        p = self.get_patient(form)

        # TODO SHould we verify that this patient has an appointment today and that they have arrived in neighborhood of scheduled time?
        # get all active appointments for this patient today and set status to Checked In
        patient_appts = Appointments.get_appointments_for_patient(patient_id=p.id)
        for appt in patient_appts:
            if Appointments.is_active(appt):
                appt.status = 'Checked In'
        return p





class PatientInfoView (FormView):
    form_class = PatientInfoForm
    template_name = 'patient_info.html'
    success_url = reverse_lazy('kiosk')

    def get(self, request, patient_id):
        p = Patient(id=patient_id)
        f = self.form_class(p.data)
        return render(request, self.template_name, {'fname': p.first_name, 'form': f})

    def post(self, request, patient_id):
        # TODO would like to include question about Are there any recent health changes we should
        # know about today?  - Answer would be appended to the appt.reason  field
        form = self.form_class(request.POST)
        if form.is_valid():
            recent_chg = form.cleaned_data['recent_changes']
            if recent_chg:
                # TODO find first active future appt for this patient today and append this to the reason field.
                pass
            return redirect(self.success_url)
        else:
            render(request, self.template_name,{'form': form})


class CheckoutSurveyView(FormView):
    form_class = CheckoutSurveyForm
    template_name = 'checkout.html'
    success_url = reverse_lazy('kiosk')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request,self.template_name, {'form': form})

    def post (self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        return redirect(self.success_url)