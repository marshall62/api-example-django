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
    rating = forms.CharField(label="Rate today's visit (1-5)")
    ontime = forms.CharField(label="The doctor was on-time (disagree - agree)")
    spent_time = forms.CharField(label="The doctor spent adequate time with me (disagree - agree)")
    issues_addressed = forms.CharField(label="The issues and questions I had were well addressed (disagree - agree)")
    support_efficient = forms.CharField(label="The support staff was friendly and efficient (disagree - agree)")
    will_return = forms.CharField(label="Todays appointment met my needs and I will return to this doctor in the future(disagree - agree)")




class PatientInfoForm (forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    date_of_birth = forms.DateField(required=False)
    gender = forms.CharField()
    address = forms.CharField(required=False)
    prefer_verbal = forms.BooleanField(label="I prefer to ask questions and raise issues with my doctor personally")
    recent_changes = forms.CharField(widget=forms.Textarea,
                                     label='Describe any recent changes to your health',
                                     required=False)
    other_med_info = forms.CharField(widget=forms.Textarea,
                                     label='Is there info from other medical appointments or doctors that we might not have received that '
                                           'is important for us in today\'s visit?',
                                     required=False)
    patient_issues = forms.CharField(widget=forms.Textarea,
                                     label='Do you have any questions or issues about your health that you really want addressed today?  If so, what are they?',
                                     required=False)