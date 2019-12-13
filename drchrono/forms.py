from django import forms
from django.forms import widgets
import re

# Add your forms here
class CheckinForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    ssn4 = forms.CharField(max_length=4, label='Last 4 digits of SSN', required=False)

    def clean_ssn4 (self):
        ssn4 = self.cleaned_data['ssn4']
        if len(ssn4) > 0:
            ssn_valid = re.match("\d{4}$",ssn4)
            if not ssn_valid:
                raise forms.ValidationError("SSN must be 4 digits")
        return ssn4

class CheckoutSurveyForm(forms.Form):
    rating = forms.FloatField(label="Rate today's visit (1-5)")
    # ontime = forms.CharField(label="The doctor was on-time (disagree - agree)")
    # spent_time = forms.CharField(label="The doctor spent adequate time with me (disagree - agree)")
    # issues_addressed = forms.CharField(label="The issues and questions I had were well addressed (disagree - agree)")
    # support_efficient = forms.CharField(label="The support staff was friendly and efficient (disagree - agree)")
    # will_return = forms.CharField(label="Overall rating of todays appointment")




class PatientInfoForm (forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    date_of_birth = forms.DateField(required=False)
    gender = forms.CharField()
    address = forms.CharField(required=False)
    # prefer_verbal = forms.BooleanField(label="I prefer to ask questions and raise issues with my doctor personally")
    # recent_changes = forms.CharField(
    #                                  label='Describe any recent changes to your health',
    #                                  required=False)
    # other_med_info = forms.CharField(
    #                                  label='Medical tests or info?',
    #                                  required=False)
    # patient_issues = forms.CharField(
    #                                  label='Questions or Issues you want addressed today?',
    #                                  required=False)